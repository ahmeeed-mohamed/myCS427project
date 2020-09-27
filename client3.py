import socket
from cryptography.fernet import Fernet
import random
import itertools


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5003  # socket server port number
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))# connect to the server
    
    n = random.randint(0,22)#generate random anounce
    message = input(' -> ')  # take input
    huge_list = []
    with open('key.txt', "r") as f:
          for line in f:
            huge_list.extend(line.split())
    list_cycle = itertools.cycle(huge_list)
    for i in huge_list:
        if i == message:
            next(list_cycle)
            next_element = next(list_cycle)
            key = next_element
            print(key)
            f = Fernet(key)
            message2 = bytes(str(n),'utf-8')
    #first step with andrew 
            encrypted1 = f.encrypt(message2)#encrypt Na
            message1= bytes(message ,'utf-8')
            client_socket.send(message1)# send message
            client_socket.send(message2)
            print("sending identefier and Na")

    #second step with andrew 
            data1 = client_socket.recv(1024).decode()# receive response
            message = bytes(data1 ,'utf-8')
            decrypted1 = f.decrypt(message)
            x = str(decrypted1.decode()).split(",")
            print(x)
            decrypted1 = x[0]
            decrypted2 = x[1]
            print('Received from server get Na+1 :'+decrypted1)
            print('Received from server GET Nb : '+decrypted2)

    #third step with andrew 
            m=int(decrypted2)
            m = m+1
            message3 = bytes(str(m) ,'utf-8')
            encrypted3 = f.encrypt(message3)
            client_socket.send(encrypted3)

    #fourth step with andrew     
            data3 = client_socket.recv(1024).decode()
            message4 = bytes(data3 ,'utf-8')
            decrypted3 = f.decrypt(message4)
            print('Received from server GET kab:' + str(decrypted3.decode()))  # show in terminal
            key1=decrypted3
            f = Fernet(key1)

    #get the numbers from the user to make the function work
            message5 = input("enter your first intger: ")  # again take input
            message6 = input("enter your second intger: ")  # again take input
            q=int(message5)
            k=int(message6)
            message5 = bytes(str(q) ,'utf-8')
            message6 = bytes(str(k) ,'utf-8')
            encrypted4 = f.encrypt(message5)
            encrypted5 = f.encrypt(message6)
            client_socket.send(encrypted4)
            client_socket.send(encrypted5)

    #get the multiplaction result from the server 
            data4 = client_socket.recv(1024).decode()
            message4 = bytes(data4 ,'utf-8')
            decrypted4 = f.decrypt(message4)
            print('Received from server the result of multiplacation:' + str(decrypted4.decode()))  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
