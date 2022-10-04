# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 16:48:54 2022

@author: user
"""

from flask import Flask
import json
from flask_cors import CORS
import random
from ClientSender import Sender
from ClientReceiver import Receiver
from EnergyClient import EnergyClient
from threading import Thread
import time
import pandas as pd
app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/status')
def status():
    #get_info()
    return '1'
	
@app.route('/getInfo')
def get_info():
    f = open('data_info.json')
    data = json.load(f)
    return data

@app.route('/getEnergy')
def getenergy():
    df = pd.read_csv('energy.csv')
    df = df.sample(n = 300)
    result = {}
    result['actual'] = list(df['train_actual'].values)
    result['predicted'] = list(df['train_predicted'].values)
    json_object = json.dumps(result, indent=4)
    return result
    
@app.route('/startClient')
def startClient():
    print("Waiting for Configuration")
    r = Receiver()
    thread = Thread(target=r.recieve_configurations)
    thread.start()
    thread.join()
    time.sleep(20)
    e = EnergyClient()
    e.start()
    return '1'



@app.route('/getTemperature')
def getTemperature():
    df = pd.read_csv('temperature.csv')
    df = df.sample(n = 300)
    result = {}
    result['actual'] = list(df['train_actual'].values)
    result['predicted'] = list(df['train_predicted'].values)
    json_object = json.dumps(result, indent=4)
    return result

def ActivateApp():
    app.run(host='0.0.0.0', port=5001)
    
    
ActivateApp()
    
    