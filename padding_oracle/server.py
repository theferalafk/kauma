import socket
from crypto_util import unpad, encrypt, BLOCK_SIZE


HOST = "127.0.0.1"
PORT = 3874

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #schönere funktion finden
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print("running")
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
                padded_pt = encrypt(iv, ct)
                if unpad(padded_pt):
                    response.append(b'\x01')
                    print("received iv: ", iv)
                    print("received ct: ", ct)
                    print("\tpadded: ", padded_pt)
                    print("\tunpadded: ", unpad(padded_pt))
                else:
                    response.append(b'\x00')
            conn.send(b''.join(response))
            
