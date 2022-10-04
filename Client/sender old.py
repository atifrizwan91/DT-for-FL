# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 23:21:22 2022

@author: user
"""

import os
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import subprocess
import platform
import json
import compress_json
import time
from csv import writer
import requests
import socket
import threading

class sender():
    
    def __init__(self, file_name):
        self.sock = self.prepare_socket()
        self.file_name = file_name
        self.FORMAT = "utf-8"
    
    
    def prepare_socket(self):
        #conf = self.get_configuration()
        self.serverIP = "192.168.0.75"  #conf['serverIP']
        self.serverPort = "12890" #conf['port']
        ADDR = (self.serverIP, self.serverPort)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(ADDR)
        return sock
    
    def send_file(self):
        
        file_size = os.path.getsize(self.file_name)
        file = open(self.file_name, "r")
        data = file.read()
        self.sock.send(self.file_name.encode(self.FORMAT))
        

    def get_configuration(self):
        with open('config.json') as json_file:
             conf = json.load(json_file)
        return conf
    
    def send_model(self):
        payload = compress_json.load("model.json.gz")
        payload = json.loads(payload)
        # print(payload)
        r = requests.post('http://'+self.serverIP + ":" + self.serverPort + "/clientModel", payload)
       # print(f"Status Code: {r.status_code}, Response: {r.json()}")
    

    def send_using_sockets(self):
        bind_ip = ''
        bind_port = 9999
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((bind_ip, bind_port))
        server.listen(5)
        
        print("[*] Listening on {}:{}".format(bind_ip, bind_port))
        while True:
            client, addr = server.accept()
            print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
          
         

s = sender('')
s.send_model()