from pwn import *

#p = process("./chall_patched")
p = remote("0.cloud.chals.io", 22980)


p.sendline(b"up")
p.sendline(b"up")
p.sendline(b"down")
p.sendline(b"down")
p.sendline(b"left")
p.sendline(b"right")
p.sendline(b"left")
p.sendline(b"right")
p.recvuntil(b"Should we go left, right, up, or down?")
p.interactive()

#11
