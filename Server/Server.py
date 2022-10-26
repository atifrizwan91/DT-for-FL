# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:20:38 2022

@author: user
"""
import json
import numpy as np
from ServerSender import Sender
from ServerReceiver import Receiver
from threading import Thread
import time
from pathlib import Path
import pandas as pd
from csv import writer
import compress_json
from termcolor import colored
from Configuration import Configuration
import math
class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Server():
    
    def __init__(self):
        conf = self.get_conf()
        self.clients = conf['clients']
        self.num_of_clients = len(self.clients)
        self.clients_IPs = conf['clients_IPs']
        self.clients_Ports = conf['clients_Ports']
        self.model = conf['model']
        self.server_rounds = conf['server_rounds']
        self.initilize_()
        self.selected_clients = self.clients
        self.completed_rounds = 0
        if(len(self.clients) != len(self.clients_IPs) or len(self.clients_IPs) !=len(self.clients_Ports)):
            print('Error: The size of clients, Ips add and ports should be equal')
        
        
        
    def initilize_(self):
        f = open('ModelReceivedList.txt', '+w')
        f.write('')
        f = open('selected Clients.txt', '+w')
        f.close()
        for i in self.clients:
            Path(i).mkdir(parents=True, exist_ok=True)
            f = open(i+'/performance.csv', '+w')
            f.close()
        
        
    def get_conf(self):
        with open('server_config.json') as json_file:
             conf = json.load(json_file)
        return conf
    
    
    def check_model_received_list(self):
        f = open('ModelReceivedList.txt', 'r')
        received_clients = f.read()
        received_clients = received_clients.split(',')
        f = set(received_clients).intersection(self.clients)
        f = len(list(f)) == self.num_of_clients
        return f
    
    
    def variance(self,data):
        n = len(data)
        mean = sum(data) / n
        deviations = [(x - mean) ** 2 for x in data]
        v = sum(deviations) / n
        return mean,v
    
    def partial_participation(self):
        all_clients_performance = {}
        per_for_variance = []
        for i in self.clients:
            data = compress_json.load(i + '/model.json.gz')
            data = json.loads(data)
            performance =  data['performance']
            df = pd.DataFrame(performance, columns= performance.keys())
            all_clients_performance[i] = list(df['mae'])[-1]
            per_for_variance.append(list(df['mae'])[-1])
        
        mu, v = self.variance(per_for_variance)
        sigma = math.sqrt(v)
        selected_clients = []
        for i in all_clients_performance:
            if(all_clients_performance[i] < mu+1*sigma):
                selected_clients.append(i)
        f = open('selected Clients.txt', '+a')
        writer_object = writer(f)
        writer_object.writerow(selected_clients)
        f.close()
        self.selected_clients = selected_clients
        return selected_clients
            
    def get_weights(self, client):
         # with open(client + '/model.json') as json_file:
         data = compress_json.load(client + '/model.json.gz')
         data = json.loads(data)
         weights = np.array([np.array(i) for i in data['weights']])
         performance =  data['performance']
         df = pd.DataFrame(performance, columns= performance.keys())
         
         if(self.completed_rounds == 1):
             df.to_csv(client+ '/performance.csv', mode='w', header=True)
         else:
             df.to_csv(client+ '/performance.csv', mode='a', header=False)
             print('Appending perfrormanceto CSV')
         return weights
        
    def collect_weights(self):
        all_weights = []
        selected_clients = self.partial_participation() #self.clients for full client participation
        print(selected_clients)
        print('--------------------')
        for i in selected_clients:
            weights = weights = self.get_weights(i)
            print(i+' Selected')
            all_weights.append(weights)
        return all_weights
    
    def average_weights(self, weights):
        return np.mean(weights, axis=0)
    
    def aggregate_weights(self,weights):
        aggregated_weights = []
        for i in range(0, len(weights[0])):
            t = []
            for c in range(0, len(self.selected_clients)): #self.num_of_clients
                t.append(weights[c][i])
            aggregated_weights.append((self.average_weights(t)))
        #self.save_model_json(aggregated_weights)
        return aggregated_weights
    
    def save_model_json(self, weights):
        payloads = {'weights': weights}
        payloads = json.dumps(payloads, cls=NumpyEncoder)
        compress_json.dump(payloads, 'aggregated_model.json.gz')
        # with open('aggregated_model.json', 'w') as server_dir:
        #     server_dir.write(payloads)
    
    def send_model_to_clients(self):
        s = Sender('aggregated_model.json.gz')
        s.BROADCAST()
    
    def start_receiver(self):
        r = Receiver()
        thread = Thread(target=r.paraller_receiver)
        thread.start()
        
    def start(self):
        self.start_receiver()
        rounds = 1
        while(rounds <= self.server_rounds):
            print('--------------Waiting for Clients-------------------')
            flag = self.check_model_received_list()
            if(flag):
                print('--------------[Server Round ' +str(rounds) +'--------------')
                weights = self.collect_weights()
                aggregated_weights = self.aggregate_weights(weights)
                self.save_model_json(aggregated_weights)
                self.send_model_to_clients()
                #self.initilize_()
                self.completed_rounds = rounds
                rounds += 1
                f = open('ModelReceivedList.txt', 'w')
                f.write('')
            time.sleep(10)
                


print('-------------Preparing Configuration Files')
c = Configuration()
c.setup_configurations()
print('Sending Configurations')
s = Sender('config.json')
s.Broadcast_Configurations()
time.sleep(1)
s = Server()
s.start()