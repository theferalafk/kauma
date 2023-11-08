import socket
from crypto_util import unpad, decrypt, BLOCK_SIZE


HOST = "127.0.0.1"
PORT = 3874
VERBOSE = False
if __name__ == "__main__":
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.create_server((HOST, PORT)) as s:
        #schönere funktion finden
        print("running")
        #s.bind((HOST, PORT))
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
                    padded_pt = decrypt(iv, ct)
                    result = unpad(padded_pt)
                    if result or result==b'':
                        response.append(b'\x01')
                        if VERBOSE:
                            print("received iv: ", iv)
                            print("received ct: ", ct)
                            print("padded: ", padded_pt)
                            print("unpadded: ", unpad(padded_pt))
                    else:
                        response.append(b'\x00')
                conn.sendall(b''.join(response))
            
