import socket
from crypto_until import encrypt, pad

host = "127.0.0.1"
port = 3874

def send_oracle_protocol(host, port, n_blocks, ct, iv_list):
    res = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(ct)
        s.send(n_blocks.to_bytes(2, byteorder='little'))
        for iv in iv_list:
            s.send(iv)
        res = s.recv(n_blocks)
        s.close()
    return res

if __name__ == "__main__":
    ct = encrypt(b'\x12\x34'*8, b'chacha20ply1305')
    iv_list = []
    n = 10
    for i in range(n):
        iv_list.append(b'12356789012345'+i.to_bytes(1, byteorder='little'))
    print(send_oracle_protocol("127.0.0.1", 3874, n, ct, iv_list))