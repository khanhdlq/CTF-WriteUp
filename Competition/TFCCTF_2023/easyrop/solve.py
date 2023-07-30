#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("easyrop_patched")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./easyrop_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./easyrop_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def write(idx, data):
    sla(b'to read!', str(1))
    sla(b'Select index: ', str(idx))
    sla(b'Select number to write: ', str(data))

def read(idx):
    sa(b'to read!', str(2))
    sla(b'Select index: ', str(idx))
for i in range(10): 
    write(i+1, str(i*100))


p.interactive()