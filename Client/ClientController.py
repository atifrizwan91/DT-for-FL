# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 14:53:46 2022

@author: user
"""

from EnergyClient import EnergyClient
from threading import Thread
from ClientReceiver import Receiver
import time


def start_client():
    
    r = Receiver()
    thread = Thread(target=r.recieve_configurations)
    thread.start()
    thread.join()
    time.sleep(20)
    e = EnergyClient()
    e.start()

def get_configurations():
    print("Waiting for Configuration")
    
    

