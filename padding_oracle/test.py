from exploit_oracle import oracle_solver
from crypto_util import encrypt, decrypt, pad, unpad

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 3874
    iv = b'a1b2c3d4e5f6g7h8'
    padded_pt = pad(b'djbernstein')
    ct = encrypt(iv, padded_pt)
    print(padded_pt)
    print(oracle_solver(host, port, iv, ct))