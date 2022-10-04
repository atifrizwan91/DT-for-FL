# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 22:59:24 2022

@author: user
"""

from flask import Flask
import json
from flask_cors import CORS
import random
from EnergyClient import *
from threading import Thread
from flask import request
import pandas as pd
app = Flask(__name__)
CORS(app)



@app.route('/start')
def start():
    e = EnergyClient() 
    # e.start()
    thread = Thread(target = e.start())
    thread.start()
    thread.join()


@app.route('/clientresults')
def results():
    df = pd.read_csv('performance.csv')
    result = df.to_dict()
    json_object = json.dumps(result, indent=4)
    return result

@app.route('/aggregatedmodel')
def aggregated_model():
    model = request.data
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)