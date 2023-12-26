from pwn import*

p = process(["./col",b"a"*20])

gdb.attach(p, gdbscript='''
b*main
c
''')

p.interactive()