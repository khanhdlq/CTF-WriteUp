from hashlib import md5
byte=[]
def encrypt(plaintext, key):
    key = md5(key).digest()
    msg = plaintext + b'|' + key
    print(len(msg))
    encrypted = b'K'
    for i in range(len(msg)):
        encrypted += bytes([(msg[i] + key[i%len(key)]  + encrypted[i]) & 0xff])
    return encrypted.hex()
for i in range(33,126):
    for j in range(33,126):
        key = b"zmze" + bytes([i]) + bytes([j]) + b"a" * 31
        print(chr(i)+chr(j))
        flag = b"KMA{" + key + b"}"
        cypher = b"4b851cc4cdd1c7a3b7a3d83095a46a320e6b21e9e5afab7b8869d930c9cd981a0523a037faca8425f9a921c6ebca8f7087f8aab5bc53fe9cd5acfa9e"
        ciphertext = encrypt(flag, key)
        print(ciphertext)
#4b851cc4cdd1c7a3b7a3d83095a46a320e6b21e9e5afab7b8869d930c9cd981a0523a037faca8425f9a921c6ebca8f7087f8aab5bc53fe9cd5acfa9e
