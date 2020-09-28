import socket
from cryptography.fernet import Fernet
import random
import itertools


def my_function(x,y):
  return x * y


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5003  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        # receive id
        data1 = conn.recv(1024).decode()
        if not data1:
          print("close connection")
          break
        message1 = data1
        huge_list = []
        #search on the file for id 
        with open('key.txt', "r") as fi:
          for line in fi:
            huge_list.extend(line.split())
        list_cycle = itertools.cycle(huge_list)
        #get the key of the id 
        id_found = False 
        for i in huge_list:
          if i == message1:
            next(list_cycle)
            next_element = next(list_cycle)
            key = next_element
            id_found=True
        if (  id_found == True):
         print(key)
         f = Fernet(key)
         #first step with andrew
         data2 = conn.recv(1024).decode()
         print(data2)
         print("from connected user get identefier: " + message1)
         print("from connected user get Na " + str(data2))

        #second step with andrew
         m=int(data2)
         n = random.randint(0,22)#generate random annoucment 
         m = m+1 
         message = str(m)+","+str(n)
         message1 = bytes(str(message) ,'utf-8')
         f = Fernet(key)
         encrypted1 = f.encrypt(message1)
         conn.send(encrypted1)  # send data to the client
         print("sending Na+1")
         print("sending Nb")
         #third step with andrew 
         data3 = conn.recv(1024).decode()
         message3 = bytes(data3 ,'utf-8')
         decrypted3= f.decrypt(message3)
         if (int(decrypted3.decode()) == n+1):
              print("from connected user get Nb+1 " + str(decrypted3.decode()))
              #fourth step with andrew     
              key2 = Fernet.generate_key()
              encrypted3 = f.encrypt(key2)
              conn.send(encrypted3)
              print("andrew protocol is succsesfull contenue")
              #receive the parameters of the procedure               
              f = Fernet(key2)
              data4 = conn.recv(1024).decode()
              data5 = conn.recv(1024).decode()
              message4 = bytes(data4 ,'utf-8')
              message5 = bytes(data5 ,'utf-8')
              decrypted4= f.decrypt(message4)
              n1=int(decrypted4)
              decrypted5= f.decrypt(message5)
              n2=int(decrypted5)
              print("from connected user get n1: " + str(decrypted4.decode()))
              print("from connected user get n2: " + str(decrypted5.decode()))

              #call procedure
              mult=my_function(n1,n2)
              #send the function result to the client 
              print("multiplcatin result is: " + str(mult))
              message6 = bytes(str(mult) ,'utf-8')
              encrypted4 = f.encrypt(message6)
              conn.send(encrypted4)
         else:
              print("authentication failed: Nb+1 not correct")
        else:
            print("authentication failed: id not found")
    conn.close()  # close the connection

          
            

if __name__ == '__main__':
    server_program()
