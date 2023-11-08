import socket
from padding_oracle.crypto_util import encrypt, pad

def send_oracle_protocol(host, port, ct, iv_list):
    res = b''
    with socket.create_connection((host, port)) as s:
        #schönere funktion finden
        s.sendall(ct)
        n_blocks = len(iv_list)
        s.sendall(n_blocks.to_bytes(2, byteorder='little'))
        for iv in iv_list:
            s.sendall(iv)
        res = s.recv(n_blocks)
    return res

if __name__ == "__main__":
    ct = encrypt(b'\x12\x34'*8, pad(b'chacha20ply1305'))
    iv_list = []
    n = 256
    for i in range(n):
        iv_list.append(b'123567890123456'+i.to_bytes(1, byteorder='little'))
    print(send_oracle_protocol("127.0.0.1", 3874, n, ct, iv_list))