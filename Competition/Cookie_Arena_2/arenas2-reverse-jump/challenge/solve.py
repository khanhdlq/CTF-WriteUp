#!/usr/bin/python3
import pefile
from pwn import *
import subprocess
elf = pefile.PE("jump.exe")



local = True 
if local:
    p = subprocess.Popen(["./jump.exe"])
    gdb.attach(p,'''''')
else:
    p = remote('chall.pwnable.tw', 10001)

flag = 0x00401500
#p.sendafter(b'jump:', p64(flag))
p.interactive()