# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:34:58 2022

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 23:21:22 2022

@author: user
"""

import os
import json
import socket
import time
from threading import Thread

class Sender():
    
    def __init__(self, file_name):
        
        
        conf = self.get_configuration()
        # self.sock = self.prepare_socket()
        self.file_name = file_name
        self.FORMAT = "utf-8"
        self.clients = conf['clients']
        self.clients_IPs = conf['clients_IPs']
        self.clients_Ports = conf['clients_Ports']
        self.sock = None
    
    # def prepare_socket(self):
    #     conf = self.get_configuration()
    #     self.serverIP = conf['serverIP']
    #     self.DeviceId = conf['DeviceId']
    #     self.serverPort = 5000 #conf['port']
    #     ADDR = (self.serverIP, self.serverPort)
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.connect(ADDR)
    #     return sock
    
    def prepare_socket(self, Addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(Addr)
        print('Connected to')
        print(Addr)
        return sock
    
    
    # def test(self):
    #     ips = self.clients_IPs.copy()
    #     ports = self.clients_Ports.copy()
        
    #     while(len(ips) != 0):
    #         sock = self.prepare_socket((ips[i],ports[i]))
            
        
        
    
    
    def BROADCAST(self):
        i = 0
        print('-------------------Broadcasting Aggregated Model---------------------')
        while(i < len(self.clients)):
                #sock = self.prepare_socket((self.clients_IPs[i],self.clients_Ports[i]))
                #self.SendModel(self.clients_IPs[i],self.clients_Ports[i])
            thread = Thread(target=self.SendModel, args=(self.clients[i],self.clients_IPs[i],self.clients_Ports[i],))
            thread.start()
            i += 1
    
    def SendModel(self,client_id ,ip, port):
        hit_rate = 1
        while(True):
            try:
                #prepare socket
                sock = self.prepare_socket((ip,port))
                #Send File name
                sock.send(self.file_name.encode(self.FORMAT))
                print(sock.recv(1024).decode(self.FORMAT))
                
                #Send File Size
                file_size = os.path.getsize(self.file_name)
                sock.send(str(file_size).encode(self.FORMAT))
                print(sock.recv(1024).decode(self.FORMAT))
                
                
                #Send Model
                
                c = 0
                packet_size = 1024
                with open(self.file_name, "rb") as file:
                    while c <= file_size:
                        data = file.read(packet_size)
                        if not (data):
                            break
                        sock.sendall(data)
                        #print('Send Data' +str(c))
                        c += len(data)
                        if(file_size-c <packet_size):
                            packet_size = file_size-c

                # file = open(self.file_name, "r")
                # data = file.read()
                # self.sock.send(data.encode(self.FORMAT))
                
                
                print(sock.recv(1024).decode(self.FORMAT))
                sock.close()
                break
            except:
                print('Error: Node  [--'+ client_id +'--] Running on [' + ip + ':'+str(port) +'] is down')
                print('Trying to approach again [--' + client_id + '--] After 10 seconds- Attempt Number: '+ str(hit_rate))
                hit_rate += 1
                if(hit_rate > 5):
                    break
                time.sleep(20)
    
    
    
    def Broadcast_Configurations(self):
        i = 0
        

        clients = self.clients

        while(i < len(clients)):
                #sock = self.prepare_socket((self.clients_IPs[i],self.clients_Ports[i]))
                #self.SendModel(self.clients_IPs[i],self.clients_Ports[i])
            thread = Thread(target=self.SendConfigurations, args=(self.clients[i],self.clients_IPs[i],self.clients_Ports[i],))
            thread.start()
            i += 1
            
    def SendConfigurations(self,client_id ,ip, port):
        print('--------------Broadcasting Configurations---------------')
        hit_rate = 1
        while(True):
            try:
                #prepare socket
                sock = self.prepare_socket((ip,port))
                #Send File name
                
                sock.send(self.file_name.encode(self.FORMAT))
                print(sock.recv(1024).decode(self.FORMAT))
                
                #Send File Size
                
                file_size = os.path.getsize(client_id +'/' +self.file_name)
                sock.send(str(file_size).encode(self.FORMAT))
                print(sock.recv(1024).decode(self.FORMAT))
                
                
                #Send Model
                
                c = 0
                packet_size = 1024
                print('Sending '+ client_id +'/' +self.file_name)
                
                with open(client_id +'/' +self.file_name, "rb") as file:
                    while c <= file_size:
                        data = file.read(packet_size)
                        if not (data):
                            break
                        sock.sendall(data)
                        #print('Send Data' +str(c))
                        c += len(data)
                        if(file_size-c <packet_size):
                            packet_size = file_size-c

                # file = open(self.file_name, "r")
                # data = file.read()
                # self.sock.send(data.encode(self.FORMAT))
                
                
                print(sock.recv(1024).decode(self.FORMAT))
                sock.close()
                break
            except:
                print('Error: Node  [--'+ client_id +'--] Running on [' + ip + ':'+str(port) +'] is down')
                print('Trying to approach again [--' + client_id + '--] After 10 seconds- Attempt Number: '+ str(hit_rate))
                hit_rate += 1
                if(hit_rate > 5):
                    break
                time.sleep(15)
    # def BROADCAST(self):
    #     i = 1
    #     hit_rate = 1
    #     while(i <= len(self.clients)):
    #         try:
    #             self.sock = self.prepare_socket((self.clients_IPs[i],self.clients_Ports[i]))
    #             #Send File name
    #             self.sock.send(self.file_name.encode(self.FORMAT))
    #             print(self.sock.recv(1024).decode(self.FORMAT))
                
    #             #Send File Size
    #             file_size = os.path.getsize(self.file_name)
    #             self.sock.send(str(file_size).encode(self.FORMAT))
    #             print(self.sock.recv(1024).decode(self.FORMAT))
                
                
    #             #Send Model
                
    #             c = 0
    #             packet_size = 1024
    #             with open(self.file_name, "rb") as file:
    #                 while c <= file_size:
    #                     data = file.read(packet_size)
    #                     if not (data):
    #                         break
    #                     self.sock.sendall(data)
    #                     #print('Send Data' +str(c))
    #                     c += len(data)
    #                     if(file_size-c <packet_size):
    #                         packet_size = file_size-c
                
                
                
                
    #             # file = open(self.file_name, "r")
    #             # data = file.read()
    #             # self.sock.send(data.encode(self.FORMAT))
                
                
    #             print(self.sock.recv(1024).decode(self.FORMAT))
    #             self.sock.close()
    #             hit_rate = 0
    #         except:
    #             print('Error: Node '+ self.clients[i] +' Running on ' + self.clients_IPs[i]+ ':'+str(self.clients_Ports[i]) +' is down')
    #             print('Trying to approach node ' +self.clients[i]+ ' After 10 seconds- Attempt Number: '+ str(hit_rate))
    #             hit_rate += 1
    #             if(hit_rate < 5):
    #                 i -= 1
                
    #             time.sleep(10)
        
                
                
    # def send_file(self):
    #     #Send DeviceId
    #     # self.sock.send(self.DeviceId.encode(self.FORMAT))
    #     # print(self.sock.recv(1024).decode(self.FORMAT))
        
        
    #     #Send File name
    #     self.sock.send(self.file_name.encode(self.FORMAT))
    #     print(self.sock.recv(1024).decode(self.FORMAT))
        
    #     #Send File Size
    #     file_size = os.path.getsize(self.file_name)
    #     self.sock.send(str(file_size).encode(self.FORMAT))
    #     print(self.sock.recv(1024).decode(self.FORMAT))
        
    #     #Send File Content
    #     file = open(self.file_name, "r")
    #     data = file.read()
    #     self.sock.send(data.encode(self.FORMAT))
    #     print(self.sock.recv(1024).decode(self.FORMAT))

    def get_configuration(self):
        with open('server_config.json') as json_file:
              conf = json.load(json_file)
        return conf
    
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
          
         

# s = Sender('aggregated_model.json.gz')
# s.BROADCAST()