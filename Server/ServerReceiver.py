# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:34:33 2022

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 16:40:18 2022

@author: user
"""


import socket
import json
from threading import Thread
class Receiver():
    def __init__(self):
        conf = self.get_configuration()
        self.FORMAT = "utf-8"
        self.rounds = 0
        self.serverPort = 5000 #conf['serverPort']
        #self.sock = self.prepare_socket(5000)
        
    def prepare_socket(self,serverPort):
        
        self.serverIP =  '' # conf['serverIP']
        #self.serverPort = 5000 # conf['serverPort']
        ADDR = (self.serverIP,serverPort)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(ADDR)
        sock.listen()
        print("[LISTENING] Server is listening. IP:" + self.serverIP +"Port:"+ str(serverPort))
        return sock
    
    def get_configuration(self):
        with open('server_config.json') as json_file:
             conf = json.load(json_file)
        return conf
    
    def update_received_list(self, DeviceId):
        f = open('ModelReceivedList.txt', 'a')
        f.write(',' + str(DeviceId))
        f.close()
        
    def recieve(self):
        
        while True:
            conn, addr = self.sock.accept()
            if(addr):
                self.rounds += 1
                #Receive Device ID
                DeviceId = conn.recv(1024).decode(self.FORMAT)
                conn.send("DeviceId  Received By Server".encode(self.FORMAT))
                print(DeviceId)
                #Receive File Name
                filename = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Name Received By Server".encode(self.FORMAT))
                print(filename)
                #Receive File Size
                filezsize = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Size Received By Server".encode(self.FORMAT))
                print(filezsize)
                c = 0
                #Receive File Content
                packet_size = 1024
                filezsize = int(filezsize)
                with open(DeviceId+'/'+filename, "+wb") as file:
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
                # file = open(DeviceId+'/'+filename, "+w")
                # file.write(data)
                
                
                conn.send("File data received By Server".encode(self.FORMAT))
                file.close()
                print('Data Received From Client')
                self.update_received_list(DeviceId)
                
    # Different port for each node
    def paraller_receiver(self):
        with open('receiving_ports.json') as json_file:
             receiving_ports = json.load(json_file)
        
        #receiving_ports = json.load(receiving_ports)
        for node in receiving_ports:
            ip = receiving_ports[node][0]
            port =  receiving_ports[node][1]
            print(port)
            sock = self.prepare_socket(port)
            thread = Thread(target = self.listen_sockets, args=(sock,))
            thread.start()
            
            
    def listen_sockets(self, sock):
        while True:
            conn, addr = sock.accept()
            if(addr):
                self.rounds += 1
                #Receive Device ID
                DeviceId = conn.recv(1024).decode(self.FORMAT)
                conn.send("DeviceId  Received".encode(self.FORMAT))
                print(DeviceId)
                #Receive File Name
                filename = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Name Received".encode(self.FORMAT))
                print(filename)
                #Receive File Size
                filezsize = conn.recv(1024).decode(self.FORMAT)
                conn.send("File Size Received".encode(self.FORMAT))
                print(filezsize)
                
                #Receive File Content
                c = 0
                packet_size = 1024
                filezsize = int(filezsize)
                with open(DeviceId+'/'+filename, "+wb") as file:
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
                # file = open(DeviceId+'/'+filename, "+w")
                # file.write(data)
                
                
                conn.send("Model received".encode(self.FORMAT))
                file.close()
                print('Model Received from '+ str(DeviceId) + '[' + str(addr) + ']')
                self.update_received_list(DeviceId)
        
# r = Receiver()
# r.paraller_receiver()