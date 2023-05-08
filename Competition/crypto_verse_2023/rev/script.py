from web3 import Web3

w3 = Web3()

contract_address = "<contract_address>"  # Replace with the address of the contract
abi = [...]  # Replace with the ABI of the contract

contract = w3.eth.contract(address=contract_address, abi=abi)

# The first 8 bytes are fixed, so we don't need to try all possible values
prefix = b"\x34\x92\x80\x01\x00\x67\x01\x55"

for i in range(2 ** 64):
    key_bytes = prefix + i.to_bytes(8, byteorder="big") + prefix
    key = Web3.toHex(key_bytes)
    magic1 = contract.functions.magic1(int(key, 16), 16).call()
    magic2 = contract.functions.magic2(int(key[:16], 16)).call()
    if magic1 == 0x1964 and magic2 == 16:
        flag_bytes = (int(key[:16], 16) ^ contract.functions.goal().call()).to_bytes(16, byteorder="big")
        flag = Web3.toHex(flag_bytes)
        if contract.functions.checkflag(Web3.toBytes(hexstr=key), Web3.toBytes(hexstr=flag)).call():
            print(f"Found key: {key}")
            print(f"Flag: {flag}")
            break
