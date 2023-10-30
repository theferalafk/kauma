import socket
from crypto_until import encrypt, pad

host = "127.0.0.1"
port = 3874

a = 13

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    iv = b'\x0f\xf0'*8
    ct = b'hallogehtdas'
    s.send(encrypt(iv, pad(ct)))
    s.send(a.to_bytes(2, byteorder='little'))
    for i in range(a):
        s.send(i.to_bytes(1, byteorder='little')*16)
    print(s.recv(a))
    s.close()