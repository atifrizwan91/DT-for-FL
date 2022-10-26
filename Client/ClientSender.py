# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 23:21:22 2022

@author: user
"""

import os
import json
import socket
import time

class Sender():
    
    def __init__(self, file_name):
        self.sock = self.prepare_socket()
        self.file_name = file_name
        self.FORMAT = "utf-8"
    
    
    def prepare_socket(self):
        conf = self.get_configuration()
        self.serverIP = conf['serverIP']
        self.DeviceId = conf['DeviceId']
        self.serverPort = 5000 #conf['port']
        ADDR = (self.serverIP, self.serverPort)
        print('Connecting to ')
        print(ADDR)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(ADDR)
        return sock
    
    def get_configuration(self):
        with open('config.json') as json_file:
              conf = json.load(json_file)
        return conf
    
    
    def send_model(self):
        #Send DeviceId
        self.sock.send(self.DeviceId.encode(self.FORMAT))
        print(self.sock.recv(1024).decode(self.FORMAT))
        
        #Send File name
        self.sock.send(self.file_name.encode(self.FORMAT))
        print(self.sock.recv(1024).decode(self.FORMAT))
                
        #Send File Size
        file_size = os.path.getsize(self.file_name)
        self.sock.send(str(file_size).encode(self.FORMAT))
        print(self.sock.recv(1024).decode(self.FORMAT))
        f =  open('model_size.csv', '+a')
        f.write(str(file_size) +',')
        #Send File Content
        c = 0
        packet_size = 1024
        with open(self.file_name, "rb") as file:
            while c <= file_size:
                data = file.read(packet_size)
                if not (data):
                    break
                self.sock.sendall(data)
                #print('Send Data' +str(c))
                c += len(data)
                if(file_size-c <packet_size):
                    packet_size = file_size-c
                
                # file = open(self.file_name, "r")
                # data = file.read()
                # self.sock.send(data.encode(self.FORMAT))
        print(self.sock.recv(1024).decode(self.FORMAT))
        

    # def send_file_multyTry(self):
    #     #Send DeviceId
    #     hit_rate = 0
    #     while True:
    #         try:
    #             self.sock.send(self.DeviceId.encode(self.FORMAT))
    #             print(self.sock.recv(1024).decode(self.FORMAT))
    #             #Send File name
    #             self.sock.send(self.file_name.encode(self.FORMAT))
    #             print(self.sock.recv(1024).decode(self.FORMAT))
                
    #             #Send File Size
    #             file_size = os.path.getsize(self.file_name)
    #             self.sock.send(str(file_size).encode(self.FORMAT))
    #             print(self.sock.recv(1024).decode(self.FORMAT))
                
    #             #Send File Content
    #             c = 0
    #             with open(self.file_name, "rb") as file:
    #                 while c <= file_size:
    #                     data = file.read(1024)
    #                     if not (data):
    #                         break
    #                     self.sock.sendall(data)
    #                     c += len(data)
                
    #             # file = open(self.file_name, "r")
    #             # data = file.read()
    #             # self.sock.send(data.encode(self.FORMAT))
    #             print(self.sock.recv(1024).decode(self.FORMAT))
    #             break
    #         except:
    #             hit_rate += 1
    #             print('Unable to reach Server: IP: '+ self.serverIP + ':'+ str(self.serverPort))
    #             print('trying again afer 20 seconds')
    #             time.sleep(20)
    #             if(hit_rate >4):
    #                 print('Failed to reach server')
                   
    #                 break
    
    # def send_model(self):
    #     payload = compress_json.load("model.json.gz")
    #     payload = json.loads(payload)
    #     # print(payload)
    #     r = requests.post('http://'+self.serverIP + ":" + self.serverPort + "/clientModel", payload)
    #    # print(f"Status Code: {r.status_code}, Response: {r.json()}")
    

    # def send_using_sockets(self):
    #     bind_ip = ''
    #     bind_port = 9999
        
    #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     server.bind((bind_ip, bind_port))
    #     server.listen(5)
        
    #     print("[*] Listening on {}:{}".format(bind_ip, bind_port))
    #     while True:
    #         client, addr = server.accept()
    #         print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))
    #         client_handler = threading.Thread(target=self.handle_client, args=(client,))
    #         client_handler.start()
          
         

# s = Sender('model.json.gz')
# s.send_file()