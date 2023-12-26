from pwn import*

p = process(["./ch11","flag.txt"])

p.interactive()
