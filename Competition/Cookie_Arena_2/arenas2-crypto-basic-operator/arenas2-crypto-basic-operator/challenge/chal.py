from Crypto.Util import number

def padding_pkcs7(data,block_size=4):
	tmp = len(data) + (block_size - len(data) % block_size)
	return data.ljust(tmp,bytes([block_size-(len(data)%block_size)]))

def split_block(data,block_size):
	return list(int.from_bytes(data[i:i+block_size],'little') for i in range(0,len(data),block_size))

def plus_func(data,shift):
	return (data+shift)&0xffffffff

def mul_func(data,mul):
	return (data*mul)&0xffffffff

def xor_shift_right_func(data,bit_loc):
	return (data^(data>>bit_loc))&0xffffffff

def pow_func(data,e,p):
	return pow(data,e,p)

def exp_func(data,base,p):
	return pow(base,data,p)

def ecb_mode(data):
	return list(pow_func(exp_func(xor_shift_right_func(mul_func(plus_func(block,3442055609),2898124289),1),e,p),e,p) for block in split_block(padding_pkcs7(data,4),4))





def reverse_pow_func(x, e, p):
    data = 0
    for i in range(p):
        if pow(i, e, p) == x:
            data = i
            break
    return data


if __name__=='__main__':
	p = 1341161101353773850779
	e = 2
	mess = b'CHH{CENSORED}'
	Cipher = [752589857254588976778, 854606763225554935934, 102518422244000685572, 779286449062901931327, 424602910997772742508, 1194307203769437983433, 501056821915021871618, 691835640758326884371, 778501969928317687301, 1260460302610253211574, 833211399330573153864, 223847974292916916557]
	cipher_flag = ecb_mode(mess)

