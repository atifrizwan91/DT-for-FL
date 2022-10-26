# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 16:40:18 2022

@author: user
"""


import socket
import json
import time
class Receiver():
    def __init__(self,sock):
        self.sock = self.prepare_socket(sock)
        self.FORMAT = "utf-8"
        self.rounds = 0
        
    def prepare_socket(self,sock):
        conf = self.get_configuration()
        self.ClientIP =  '' # conf['serverIP']
        self.ClientPort = sock #int(input("Enter Port Number: ")) #conf['Client_port']
        ADDR = (self.ClientIP, self.ClientPort)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(ADDR)
        
        print("[LISTENING] Client is listening. IP:" + self.ClientIP + 'Client Port:' + str(self.ClientPort))
        return sock
    
    def get_configuration(self):
        with open('config.json') as json_file:
             conf = json.load(json_file)
        return conf
    
    def update_client_status(self, server_rounds):
        f = open('server_info.txt', 'a')
        f.write(',' + str(server_rounds))
        f.close()
        
        
    def recieve(self):
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            if(addr):
                self.rounds += 1
                #Receive Device ID
                # server = conn.recv(1024).decode(self.FORMAT)
                # conn.send("DeviceId  Received".encode(self.FORMAT))
                
                #Receive File Name
                filename = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Name Received By Client".encode(self.FORMAT))
                
                #Receive File Size
                filezsize = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Size Received By Client".encode(self.FORMAT))
                #print(filezsize)
                #Receive File Content
                
                c = 0
                packet_size = 1024
                filezsize = int(filezsize)
                with open('Server/'+filename, "+wb") as file:
                    while c <= int(filezsize):
                        data = conn.recv(packet_size)
                        if not (data):
                            break
                        file.write(data)
                        #print('Received '+ str(c))
                        c += len(data)
                        if(filezsize-c <packet_size):
                            packet_size = filezsize-c

                # data = conn.recv(int(filezsize)).decode(self.FORMAT)
                # file = open('Server/'+filename, "+w")
                # file.write(data)
                                
                conn.send("Model received By Client".encode(self.FORMAT))
                file.close()
                print('Model Received')
                self.update_client_status(self.rounds)
                
    def recieve_configurations(self):
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            if(addr):
                
                #Receive Device ID
                # server = conn.recv(1024).decode(self.FORMAT)
                # conn.send("DeviceId  Received".encode(self.FORMAT))
                
                #Receive File Name
                filename = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Name Received".encode(self.FORMAT))
                # print(filename)
                #Receive File Size
                filezsize = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Size Received".encode(self.FORMAT))
                #Receive File Content
                
                c = 0
                packet_size = 1024
                filezsize = int(filezsize)
                with open(filename, "+wb") as file:
                    while c <= int(filezsize):
                        data = conn.recv(packet_size)
                        if not (data):
                            break
                        file.write(data)
                        #print('Received '+ str(c))
                        c += len(data)
                        if(filezsize-c <packet_size):
                            packet_size = filezsize-c

                # data = conn.recv(int(filezsize)).decode(self.FORMAT)
                # file = open('Server/'+filename, "+w")
                # file.write(data)
                                
                conn.send("Configurations Received".encode(self.FORMAT))
                file.close()
                print('Configurations Received')
                self.sock.close()
                time.sleep(10)
                break
    # def recieve_multitry(self):
    #     self.sock.listen()
    #     while True:
    #         conn, addr = self.sock.accept()
    #         if(addr):
    #             self.rounds += 1
    #             #Receive Device ID
    #             # server = conn.recv(1024).decode(self.FORMAT)
    #             # conn.send("DeviceId  Received".encode(self.FORMAT))
                
    #             #Receive File Name
    #             filename = conn.recv(1024).decode(self.FORMAT)
    #             conn.send("File Name Received".encode(self.FORMAT))
                
    #             #Receive File Size
    #             filezsize = conn.recv(1024).decode(self.FORMAT)
    #             conn.send("File Size Received".encode(self.FORMAT))
                
    #             #Receive File Content
    #             data = conn.recv(int(filezsize)).decode(self.FORMAT)
    #             file = open('Server/'+filename, "+w")
    #             file.write(data)
    #             conn.send("File data received".encode(self.FORMAT))
    #             file.close()
    #             print('Data Received')
    #             self.update_client_status(self.rounds)
            
# r = Receiver()
# r.recieve()