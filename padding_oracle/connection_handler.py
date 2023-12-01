import socket
from padding_oracle.crypto_util import encrypt, pad

class ConnectionHandler:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_oracle_protocol(self, ct, iv_list):
        res = b''
        with socket.create_connection((self.host, self.port)) as s:
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
    ch = ConnectionHandler("127.0.0.1", 3874)
    print(ch.send_oracle_protocol(n, ct, iv_list))