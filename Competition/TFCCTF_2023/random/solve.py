#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("random")

local = False 
if local:
    p = process("./random")
    #gdb.attach(p,'''''')
else:
    p = remote('challs.tfcctf.com', 31233)

elf = context.binary = ELF('./random', checksec=False)
proc = subprocess.Popen(['./rand'],stdout=subprocess.PIPE)
line = []
line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(10):
    line[i] = int(proc.stdout.readline())
    
sleep(4)
proc = subprocess.Popen(['./rand'],stdout=subprocess.PIPE)
for i in range(10):
    line[i] = int(proc.stdout.readline())
    print(line[i])
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
sleep(0.5)
sla(b"Guess my numbers!", str(line[0]))
for i in range(9):
    sl(str(line[i+1]))
p.interactive()