#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("aftermath_patched")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./aftermath_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./aftermath_patched', checksec=False)

def add(size, data):
    p.sendlineafter(b'>', b'1')
    p.sendlineafter(b'Size:', str(size))
    p.sendafter(b'Note:', data)

def view(idx):
    p.sendlineafter(b'>', b'2')
    p.sendlineafter(b'Index:', str(idx))

def edit(idx, data):
    p.sendlineafter(b'>', b'3')
    p.sendlineafter(b'Index:', str(idx))
    p.sendafter(b'New Note:', data)


for i in range(8):
    add(0x20, str(i)*0x1f)

#edit(3, b'a'*0x1f)

p.interactive()