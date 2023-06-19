#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("Speedy")


local = False 
if local:
    p = process("./Speedy")
    #gdb.attach(p,'''''')
else:
    p = remote('0.cloud.chals.io', 34026)

elf = context.binary = ELF('./Speedy', checksec=False)

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def function1(a1, a2):
    v3 = 0
    i = 1
    while a1 >= i or a2 >= i:
        if a1 % i == 0 and a2 % i == 0:
            v3 = i
        i += 1
    return v3


def function2(a1):
    if a1:
        return a1 * function2(a1 - 1)
    else:
        return 1

def main():
    data = p.recv(1024)  # Receive data as bytes
    print(data)
    # Convert bytes to string
    data_str = data.decode()

    # Parse the values
    values = data_str.split()
    v13 = int(values[0])
    v14 = int(values[1])

    # Print the values
    print(v13, v14)
    v4 = function1(v13, v14)
    v5 = function2(v4 + 3)
    print(v5)
    sl(str(v5))
while(True):
    a = log.info('Iype:     ' + input())
    if a == 'x':
        break
    else:
        main()

p.interactive()