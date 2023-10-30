import socket
from cryptography.hazmat.primitives.padding import PKCS7

HOST = "127.0.0.1"
PORT = 3874

def encrypt():
    return 0

def decrypt():
    return 0

def pad():
    return 0

def unpad():
    return 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            print(data)