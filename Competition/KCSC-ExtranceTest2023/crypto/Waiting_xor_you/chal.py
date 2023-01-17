
def xor(a: bytes, b: bytes):
    return bytes([a[i % len(a)] ^ b[i % len(b)] for i in range(max(len(a), len(b)))])


flag = b"KCSC{???????????????????????????}"
key = b"us_oaf"
print(xor(flag, key))
c= b'>0\x0c,\x1a+:=\x100(5*,\x08*(2<=\x11!> E!\x006Q3VP"'
print(xor(c, key))