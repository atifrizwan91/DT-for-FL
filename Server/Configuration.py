# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 00:17:03 2022

@author: user
"""
import json
from pathlib import Path
import os
import pymysql
import pandas as pd

class Configuration:
    def __init__(self, database = None):
        
        if(database is None):
            self.config_from_file()
            self.deviceIds = [x for x in range(0, len(self.Ip_address))]
        else:
            print('-------------------From Database')
            self.config_from_database()
        
    def config_from_file(self):
        with open('initial_config.json') as json_file:
             conf = json.load(json_file)
        self.Ip_address = conf['Ip_address']
        self.num_clients = len(self.Ip_address)
        self.ports = conf['ports']
        self.serverIP = conf['serverIP']
        
        self.model = conf['model']
        self.data = conf['data']
        self.server_rounds = conf['server_rounds']
        self.local_epochs = conf['local_epochs']
        
        
    def config_from_database(self):
        conn = pymysql.connect(
            host='localhost',
            port=int(3306),
            user="root",
            passwd='1234',
            db="dt",
            charset='utf8mb4')
        devices = pd.read_sql_query("SELECT * FROM devices",conn)

        self.Ip_address = devices['device_ip'].values.tolist()
        self.num_clients = len(self.Ip_address)
        self.deviceIds = devices['device_id'].values.tolist()
        self.ports = [5000] * len(self.Ip_address)
        conf = pd.read_sql_query("SELECT * FROM configuration",conn)
        self.serverIP = conf['server_ip'].values.tolist()[0]
        self.model = conf['model'].values.tolist()[0]
        self.data = conf['data'].values.tolist()[0]
        self.server_rounds = conf['server_rounds'].values.tolist()[0]
        self.local_epochs = conf['local_epochs'].values.tolist()[0]
        
        
        
    def setup_configurations(self):
        for i in range(0, self.num_clients):
            conf = {
               "DeviceId": "node"+str(self.deviceIds[i]),
               "data": self.data,
               "serverIP":self.serverIP,
               "serverPort": 5000 +i,
               "model": self.model ,
               "server_rounds":self.server_rounds,
               "local_epochs":self.local_epochs
               }
            Path(conf['DeviceId']).mkdir(parents=True, exist_ok=True)
            payload = json.dumps(conf)
            f = open(conf['DeviceId']+ '/config.json', '+w')
            f.write(payload)
            f.close()
        
        nodes = []
        for i in range(0, self.num_clients):
            nodes.append("node"+str(self.deviceIds[i]))
            
        
        server_conf = {
        	"clients": nodes,
        	"clients_IPs": self.Ip_address,
           "clients_Ports":self.ports,
           "model":self.model,
           "server_rounds":self.server_rounds,
           "local_epochs":self.local_epochs
        }
        
        payload = json.dumps(server_conf)
        f = open('server_config.json', '+w')
        f.write(payload)
        f.close()
        
        #Create Sockets for Registered Clients
        Receiver_scokets = {}
        for i in range(0, self.num_clients):
            Receiver_scokets["node"+str(i)] = [self.serverIP, 5000 +i]
        
        payload = json.dumps(Receiver_scokets)
        f = open('receiving_ports.json', '+w')
        f.write(payload)
        f.close()
        

