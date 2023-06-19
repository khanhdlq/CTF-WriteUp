#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("limited_resources")

local = True 
if local:
    p = process("./limited_resources")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./limited_resources', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

p.interactive()