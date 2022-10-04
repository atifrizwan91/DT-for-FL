# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:52:21 2022

@author: user
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding, Flatten, Conv1D, SpatialDropout1D
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import os
from tensorflow.keras.callbacks import EarlyStopping
# import matplotlib.pyplot as plt
import subprocess
from pathlib import Path
import platform
import json
import compress_json
import time
# from csv import writer
from ClientSender import Sender
from threading import Thread
from ClientReceiver import Receiver
# from App import *

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

class EnergyClient:
    def __init__(self):
        conf = self.get_configuration()
        self.object_created = True
        self.data_path = 'data//'+conf['data'] +'.csv'
        self.serverIP = conf['serverIP']
        self.model_name = 'self.get_model_' + conf['model']
        self.X_train, self.X_test, self.y_train, self.y_test = self.get_seoul_data()
        self.performance = None
        self.first_iteration = True
        self.local_epochs = conf['local_epochs']
        self.current_server_round = 0
        self.server_rounds = conf['server_rounds']
        self.initilize_files()
        try:
            self.model = eval(self.model_name)()
        except:
            self.object_created = False
            print('Model ' + conf['model'] +' is not defined , Check your conf.json file')
        
        if(not self.ping(self.serverIP)):
           print('Server is down, Check your conf.json file')
           self.object_created = False
    
    def get_configuration(self):
        with open('config.json') as json_file:
             conf = json.load(json_file)
        return conf
    
    def initilize_files(self):
        f = open('server_info.txt', '+w')
        f.write('0')
        f.close()
        f = open('client_info.txt', '+w')
        f.close()
        f = open('performance.csv', '+w')
        f.close()
        Path('Server').mkdir(parents=True, exist_ok=True)
        
    def object_test(self):
        if (not self.object_created): return False
    
    def ping(self,host):
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command) == 0

    def get_data(self):
        
        df = pd.read_csv(self.data_path)
        df = df[df['Appartment']==102]
        drop = ['Building','Appartment']
        X = df.drop(drop, axis = 1)
        scaler = MinMaxScaler()
        scaler.fit(X)
        X = pd.DataFrame(scaler.transform(X),columns=['Energy','T','H'])
        y = df['Energy']
        X = X.drop('Energy', axis = 1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.03, random_state=42)
        #For LSTMCNN
        #X_train=np.array(X_train).reshape(X_train.shape[0],X_train.shape[1],-1)
        return X_train, X_test, y_train, y_test
    
    def get_seoul_data(self):
        df = pd.read_csv(self.data_path)
       
        scaler = MinMaxScaler()
        scaler.fit(df)
        df = pd.DataFrame(scaler.transform(df), columns = ['Humidity_Seoul','Seoul_Building_Agg','Temperature_Seoul','day','dayOfWeek','hour','month','year'])
        y = df['Seoul_Building_Agg']
        X = df.drop('Seoul_Building_Agg', axis = 1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.03, random_state=42)
        #For LSTMCNN
        #X_train=np.array(X_train).reshape(X_train.shape[0],X_train.shape[1],-1)
        return X_train, X_test, y_train, y_test
    
    def get_model_DNN(self):
        model=Sequential()
        model.add(Dense(units=1024, input_dim = self.X_train.shape[1], activation='relu'))
        model.add(Dense(512,activation='relu',kernel_initializer='glorot_uniform'))
        model.add(Dense(256,activation='relu',kernel_initializer='glorot_uniform'))
        model.add(Dense(128,activation='relu',kernel_initializer='glorot_uniform'))
        model.add(Dense(64,activation='relu',kernel_initializer='glorot_uniform'))
        model.add(Dense(32,activation='relu',kernel_initializer='glorot_uniform'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error',  optimizer='adam',metrics = ['mse', 'mae'])
        return model
    
    def get_LSTMCNN(self):
        
        model=Sequential()
        #print(self.X_train.shape[2],"----------------")
        #model.add(Embedding(101,256,input_length=8,))
        model.add(Conv1D(filters=128,kernel_size=5,padding='same',input_shape=(self.X_train.shape[1],self.X_train.shape[2])))
        model.add(Dense(64,activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(16,activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(1,activation='relu'))
        model.compile(loss='mean_squared_error',metrics=['accuracy'])
        return model
    
    def finetune_model(self):
        payload = compress_json.load("Server/aggregated_model.json.gz")
        payload = json.loads(payload)
        weights = np.array([np.array(i) for i in payload['weights']])
        self.model.set_weights(weights)

    def train_model(self):
        if(not  self.first_iteration):
            self.finetune_model()
       # if(not self.object_test()): return
        history = self.model.fit(self.X_train,self.y_train, epochs=self.local_epochs, batch_size=30, verbose=1, validation_data=(self.X_test,self.y_test))
        self.performance = history.history
        self.save_model_weights()
        self.save_history()
        self.first_iteration = False
        f = open('client_info.txt', 'w')
        f.write('done')
        f.close()
        
    
    def save_model_weights(self):
        weights = self.model.get_weights()
        payload = {'performance': self.performance, 'weights': weights}
        payloads = json.dumps(payload, cls=NumpyEncoder)
        compress_json.dump(payloads, 'model.json.gz')
        # with open('model.json', 'w') as local_dir:
        #     local_dir.write(payloads)
        
        
    # def model_loss(self, history):
    #     plt.figure(figsize=(8,4))
    #     plt.plot(history.history['loss'], label='Train Loss')
    #     plt.plot(history.history['val_loss'], label='Test Loss')
    #     plt.title('model loss')
    #     plt.ylabel('loss')
    #     plt.xlabel('epochs')
    #     plt.legend(loc='upper right')
    #     plt.show();
    
    def save_history(self):
        df = pd.DataFrame(self.performance)
        if(self.first_iteration):
            df.to_csv('performance.csv', mode='w',header=True)
        else:
            df.to_csv('performance.csv', mode='a', header=False)
    
    def check_termination(self):
        f = open('server_info.txt', 'r')
        st = f.read()
        print('Completed Rounds In File server_info.txt ' + st)
        rounds = st.split(',')
        if(int(rounds[-1]) != self.server_rounds):
            return False
        return True
    
    def send_model_to_server(self):
        s = Sender('model.json.gz')
        print('Sending Model')
        s.send_model()
        print('Model Transferred')
        
    def next_iteration(self):
        f = open('server_info.txt', 'r')
        st = f.read()
        rounds = st.split(',')
        if(len(rounds) == self.current_server_round):
            return False
        return True
    
    def start_receiver(self):
        r = Receiver()
        thread = Thread(target=r.recieve)
        thread.start()
        
    def start(self):
        self.start_receiver()
        
        print('Returned---------------')
        while(not self.check_termination()):
            if(self.next_iteration()):
                self.train_model()
                self.send_model_to_server()
                self.current_server_round += 1
            time.sleep(20)
            print('Waiting for Server to done')
        
    


# thread_app = Thread(target = ActivateApp)
# thread_app.start()

# print("Waiting for Configuration")
# r = Receiver()
# thread = Thread(target=r.recieve_configurations)
# thread.start()
# thread.join()
# time.sleep(20)
# e = EnergyClient()
# e.start()

