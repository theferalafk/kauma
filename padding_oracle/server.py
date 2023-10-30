import socket
from crypto_until import unpad, encrypt, BLOCK_SIZE


HOST = "127.0.0.1"
PORT = 3874

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            ct = conn.recv(BLOCK_SIZE)
            length = int.from_bytes(conn.recv(2), byteorder='little')
            iv_list = []
            for i in range(length):
                iv_list.append(conn.recv(BLOCK_SIZE))
            response = []
            for iv in iv_list:
                #hier muss noch error handling wenn blockgröße nicht erreicht ist
                print(iv, ct)
                padded_pt = encrypt(iv, ct)
                print(padded_pt)
                if unpad(padded_pt):
                    response.append(b'\x01')
                else:
                    response.append(b'\x00')
            conn.send(b''.join(response))
            conn.close()
            