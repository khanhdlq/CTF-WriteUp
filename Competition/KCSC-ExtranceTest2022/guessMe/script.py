from pwn import*
from ctypes import*

#r = remote('45.77.39.59', 10004)
p= process("guessMe_patched")
glibc = cdll.LoadLibrary('./libc6_2.27-3ubuntu1.4_amd64.so')
glibc.srand(glibc.time(None))
val = glibc.rand()

p.sendline(bytes(str(val % 1337), 'utf-8'))
p.interactive()
