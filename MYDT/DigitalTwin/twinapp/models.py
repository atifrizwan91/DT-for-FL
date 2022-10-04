from django.db import models
import requests
# Create your models here.
import pymysql
import pandas as pd
import os

IPs = ['192.168.0.66:2000']


def connect_with_Devices():
    data =requests.get(IPs[0])
    if(data.status == 'Done'):
        pass
    else:
        return data.progress
    return data

def get_connection():
    host = os.getenv('localhost')
    conn = pymysql.connect(
        host = host,
        port = int(3306),
        user = "atif",
        passwd = 'root',
        db = "dt",
        charset = 'utf8mb4')
    return conn