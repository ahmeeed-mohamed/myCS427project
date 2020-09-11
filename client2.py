import socket
from cryptography.fernet import Fernet


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5003  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    file = open('key.key', 'rb')  # Open the file as wb to read bytes
    key = file.read()  # The key will be type bytes
    file.close()
    message = input(' -> ')  # take input
    message = bytes(message ,'utf-8')

    while message.lower().strip().decode() != 'bye':
        f = Fernet(key)
        encrypted = f.encrypt(message)
        client_socket.send(encrypted)  # send message
        data = client_socket.recv(1024).decode()  # receive response
        message = bytes(data ,'utf-8')
        decrypted = f.decrypt(message)
        print('Received from server: ' + str(decrypted.decode()))  # show in terminal
        message = input(" -> ")  # again take input
        message = bytes(message ,'utf-8')
        
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
