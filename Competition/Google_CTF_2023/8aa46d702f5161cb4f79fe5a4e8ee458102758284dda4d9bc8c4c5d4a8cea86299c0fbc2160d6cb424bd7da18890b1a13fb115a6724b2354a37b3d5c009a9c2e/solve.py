#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chal")


local = True 
if local:
    p = process("./chal")
    proc = subprocess.Popen(['./rand'],stdout=subprocess.PIPE)
else:
    p = remote('ubf.2023.ctfcompetition.com', 1337)

elf = context.binary = ELF('./chal', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


sla(b'PASSWORD:', b'pencil')
sla(b'QUIT', b'1337')
sa(b'ROULETTE.', b'\x0a')
for i in range(1000):
    x = p.recvline()
    log.info(x)

    while(1):
        line = proc.stdout.readline()
        guess = int(str(line)[2:-3])
        log.info(str(i) +' ' + str(guess))
        if guess > 42: 
            s(b'\x0a')
            break
        
p.interactive()