from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from zmq import device
from twinapp.models import *
import os
import random
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding, Flatten, Conv1D, SpatialDropout1D
from tensorflow.keras.models import Sequential
import pymysql
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd

# Create your views here.

server_path = "D:/Projects/Raspberry Pi/FL Framework/Server/"


def home(request):
    return render(request, 'twinapp/DigitalTwin.html')

def devicecontrol(request):
    return render(request, 'twinapp/DeviceControl.html')

def index(request):
    return render(request, 'twinapp/Layout.html')

def registergatewaynode(request):
    return render(request, 'twinapp/RegisterGateway.html')

def deviceconnection(request):
    return render(request, 'twinapp/PreparePlatform.html')

def ClientPerfromance(request):
    return render(request, 'twinapp/ClientPerfromance.html')


def getDeviceInfo(request):
    if(request.POST.get('data_type','') == 'Temp'):
        r = round(random.uniform(20, 30),2)
    if(request.POST.get('data_type','') == 'Hum'):
        r = round(random.uniform(20, 30),2)
    if(request.POST.get('data_type','') == 'Air'):
        r = round(random.uniform(1, 3),2)
    return JsonResponse({'val': r})

def addGateway(request):
    ip_address = request.POST.get('ip_address','')
    port = request.POST.get('port','')
    con = get_connection()
    cur = con.cursor()
    query = "insert into gateways (gateway_ip, gateway_port,status) values ('"+str(ip_address)+"','"+str(port)+"',0)"
    cur.execute(query)
    con.commit()
    if(cur.rowcount == 1):
        return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})

def addDevice(request):
    ip_address = request.POST.get('ip_address','')
    port = request.POST.get('port','')
    con = get_connection()
    cur = con.cursor()
    query = "insert into devices (device_ip, port,status, gateway_num) values ('"+str(ip_address)+"','"+str(port)+"',0,1)"
    cur.execute(query)
    con.commit()
    if(cur.rowcount == 1):
        return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})
    # devices = pd.read_sql_query(query, con)

def updateConfigurations(request):
    column = request.POST.get('col','')
    value = request.POST.get('value','')
    print(column ,value)
    con = get_connection()
    cur = con.cursor()
    query = "update configuration set "+column+" = '"+value+"' where ID= 1";
    cur.execute(query)
    con.commit()
    if(cur.rowcount == 1):
        return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def get_devices_updates():
    data = connect_with_Devices()

def update_status_device():
    con = get_connection()
    cur = con.cursor()
    devices = pd.read_sql_query("SELECT * FROM devices", con)
    devices = devices.values.tolist()
    for d in devices:
        address = "http://"+str(d[1])+":"+str(d[2])+"/status"

        print(address)
        try:
            r =requests.get(address)
            q = "update devices set status = 1 where device_id ="+str(d[0])+";"
            
            print(r)
        except:
            q = "update devices set status = 0 where device_id ="+str(d[0])+";"
            print(address + " Failed")
        finally:
            cur.execute(q)
            con.commit()

def get_device_status(request):
    request_type = request.POST.get('request_type','')
    if(request_type == '1'):
        update_status_device()
    con = get_connection()
    devices = pd.read_sql_query("SELECT * FROM devices", con)
    devices = devices.values.tolist()
    return JsonResponse({'devices': devices})

#Update the status of gateway in database
def update_status_gateways():
    con = get_connection()
    cur = con.cursor()
    devices = pd.read_sql_query("SELECT * FROM gateways", con)
    devices = devices.values.tolist()
    for d in devices:
        address = "http://"+str(d[1])+":"+str(d[2])+"/status"
        print(address)
        try:
            r =requests.get(address)
            q = "update gateways set status = 1 where gateway_id ="+str(d[0])+";"
            
            print(r)
        except:
            q = "update gateways set status = 0 where gateway_id ="+str(d[0])+";"
            print(address + " Failed")
        finally:
            cur.execute(q)
            con.commit()
#Return to UI the status of gateways       
def get_gateways_status(request):

    request_type = request.POST.get('request_type','')
    if(request_type == '1'):
        update_status_gateways()
    con = get_connection()
    devices = pd.read_sql_query("SELECT * FROM gateways", con)
    devices = devices.values.tolist()
    
    return JsonResponse({'devices': devices})

def updateDeviceConnection(request):
    device_id = request.POST.get('device_id','')
    gateway_id = request.POST.get('gateway_id','')
    con = get_connection()
    cur = con.cursor()
    q = "update devices set gateway_num = "+str(gateway_id)+" where device_id ="+str(device_id)+";"
    cur.execute(q)
    con.commit()

def get_client_performance(request):
    nodeID = request.POST.get('nodeID','')
    df = pd.read_csv(server_path+nodeID+'/performance.csv')
    data = df.to_json()
    return JsonResponse({'data':data})

def getModelPerformance(request):
    df = pd.read_csv(server_path+'/performance.csv')
    df = df.drop(['Unnamed: 0','mse','val_mse'], axis = 1)
    data = df.to_html()
    return JsonResponse({'data':data})

def get_data():
        df = pd.read_csv('D:\\Projects\\Raspberry Pi\\FL Framework\\Client\\data\\Energy.csv')
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

def prepare_and_train_model(request):
    loss = request.POST.get('loss','')
    activation = request.POST.get('activation','')
    hidden_layers = request.POST.get('hidden_layers','')
    optimizer = request.POST.get('optimizer','')
    input_shape = request.POST.get('input_shape','')
    output_shape = request.POST.get('output_shape','')
    model=Sequential()
    X_train, X_test, y_train, y_test = get_data()
    print('-----------------',activation)
    model.add(Dense(units=1024, input_dim = X_train.shape[1] , activation = activation))
    for i in range(0, int(hidden_layers)):
        model.add(Dense(512,activation=activation,kernel_initializer='glorot_uniform'))
    model.add(Dense(output_shape))
    model.compile(loss=loss,  optimizer=optimizer,metrics = ['mse', 'mae'])
    
    history = model.fit(X_train,y_train, epochs=100, batch_size=30, verbose=1, validation_data=(X_test, y_test))
    df = pd.DataFrame(history.history)
    df.to_csv('performance.csv', mode='w',header=True)
    data = df.to_html()
    return JsonResponse({'data': data})