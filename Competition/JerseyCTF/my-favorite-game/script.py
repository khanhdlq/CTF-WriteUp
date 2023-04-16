from pwn import *

p = remote("0.cloud.chals.io", 22980)
p.sendline(b"up")
p.sendline(b"up")
p.sendline(b"down")
p.sendline(b"down")
p.sendline(b"left")
p.sendline(b"right")
p.sendline(b"left")
p.sendline(b"right")
p.interactive()