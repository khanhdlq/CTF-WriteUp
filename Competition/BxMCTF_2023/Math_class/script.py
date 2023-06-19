#!/usr/bin/python3
from pwn import *
import subprocess

elf = context.binary = ELF("main")
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-2.27.so")
-967057188
local = False 
if local:
    p = process("./main")
    #gdb.attach(p,'''''')
else:
    p = remote('198.199.90.158', 34762)

elf = context.binary = ELF('./main', checksec=False)
p.recvuntil(b"math!")

for i in range(5):
    arg_1 = int(p.recvuntil(b' '), )
    p.recv(2)
    arg_2 = int(p.recvuntil(b' '))
    sum = arg_1 + arg_2
    p.sendlineafter(b"?", str(sum))


sleep(3)
proc = subprocess.Popen(['./rand'], stdout=subprocess.PIPE)
summer = [0,0,0,0,0,0]
for i in range(5):
    line = proc.stdout.readline()
    line = line.decode().strip()  # Decode bytes to string and remove leading/trailing whitespaces
    numbers = line.split('=')
    number1 = int(numbers[0].strip())
    number2 = int(numbers[1].strip())
    print("Number 1:", number1)
    print("Number 2:", number2)
    summer[i] = number2 - number1
    print("Sum:", summer[i])

for i in range(5):
    p.sendline(str(summer[i]))

p.interactive()


