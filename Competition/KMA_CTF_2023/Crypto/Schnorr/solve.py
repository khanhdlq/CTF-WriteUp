from pwn import*
import random 
import time 

pp = remote('103.163.25.143', 60124)

s=int(time.time())+4
random.seed(s)
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
g = 0x2
q = 0x7fffffff800000008000000000000000000000007fffffffffffffffffffffff
y=61252110398173126436323285216974857619112851968123774381188703220254043681646


for i in range(65):
    pp.recvuntil(b'/64\n')
    c=random.randint(1,q-1)
    print("c fake = " + str(c))
    z = pow(y, c, p)
    t = pow(z, -1, p)    #tính giá trị nghịch đảo của z theo modulo p và gán kết quả vào biến t pow(y, c, p)
    pp.recvuntil(b't = ')
    pp.sendline(str(t))
    print(pp.recvuntil(b's = '))
    pp.sendline(b'0')