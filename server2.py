import socket
from cryptography.fernet import Fernet


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5003  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    key = Fernet.generate_key()
    file = open('key.key', 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        message = bytes(data ,'utf-8')
        if not data:
            # if data is not received break
            break
        f = Fernet(key)
        decrypted = f.decrypt(message)
        print("from connected user: " + str(decrypted.decode()))
        data = input(' -> ')
        message = data.encode()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        conn.send(encrypted)  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
