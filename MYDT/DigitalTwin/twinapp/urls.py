from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name = 'home'),
    path('devicecontrol', views.devicecontrol, name = 'devicecontrol'),
    path('index', views.index, name = 'index'),
    path('registergatewaynode', views.registergatewaynode, name = 'registergatewaynode'),
    path('deviceconnection', views.deviceconnection, name = 'deviceconnection'),
    path('addGateway', views.addGateway, name = 'addGateway'),
    path('addDevice', views.addDevice, name = 'addDevice'),
    path('updateConfigurations', views.updateConfigurations, name = 'updateConfigurations'),
    path('get_client_performance', views.get_client_performance, name = 'get_client_performance'),

    path('getDeviceInfo', views.getDeviceInfo, name = 'getDeviceInfo'),
    path('get_device_status', views.get_device_status, name = 'get_device_status'),
    path('get_gateways_status', views.get_gateways_status, name = 'get_gateways_status'),
    path('updateDeviceConnection', views.updateDeviceConnection, name = 'updateDeviceConnection'),
    path('ClientPerfromance', views.ClientPerfromance, name = 'ClientPerfromance'),
    path('getModelPerformance', views.getModelPerformance, name = 'getModelPerformance'),
    path('prepare_and_train_model', views.prepare_and_train_model, name = 'prepare_and_train_model'),
]
