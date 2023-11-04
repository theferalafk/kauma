from padding_oracle.exploit_oracle import oracle_solver
from padding_oracle.crypto_util import encrypt, decrypt, pad, unpad

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 3874
    iv = b'a1b2c3d4e5f6g7h8'
    padded_pt = pad(b'djbernstein')
    ct = encrypt(iv, padded_pt)
    print(ct)
    print(padded_pt)
    #print(oracle_solver(host, port, iv, ct))
    host = "141.72.5.194"
    port = 18732
    iv = 0x0478eabe443992c0b2b53cfc50aea04a.to_bytes(16, byteorder='big')
    ct = 0x566b0c7206dbb19efa9b296696af2652.to_bytes(16, byteorder='big')
    print(oracle_solver(host, port, iv, ct))
    #To-DO: Update Parser, test for \x02\x02 edge case, test random input, documentation, solve bauers things