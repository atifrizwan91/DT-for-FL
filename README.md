# Digital Twin 
## Requirements
Install VS code and setup python environment. Install following python libraries.
- django
- zmq
  - ZeroMQ is a high-performance asynchronous messaging library, aimed at use in distributed or concurrent applications.
- tensorflow
- sklearn
- pymysql
- pandas
- numpy 

Open `DT' folder in VS code and run the following commands
- `cd DigitalTwin`
- `python .\manage.py runserver`

![](https://github.com/atifrizwan91/DT-for-FL/blob/main/DT/DigitalTwin/Images/RunDT%20.png)

## Setup OCF Iotivity
 1. First of all Raspberry Pi 4 is configured and Ubuntu OS is installed
2. The Putty is used to access the IoT device from the IoT platform
3. Ubuntu is preferred instead of raspbian operating system because we have lot of support for IoTivity for ubuntu
![](https://github.com/atifrizwan91/Greenhouse/blob/main/Images/0.PNG)
- [X]  The card is then injected in the Raspberry pi to start the operating system

# Installation of required software
## Putty
1. Install putty to connect with Raspberry pi 4 remotely.
2. The putty initiate the SSH command which allow the IoT platform to send the instructions remotely
3. There are some other software are also available to use the SSH request
4. The windows terminal can also be sued to connect the IoT device with IoT Platform
![](https://github.com/atifrizwan91/Greenhouse/blob/main/Images/1.PNG)
## WINSCP
1. WinSCP is installed to move files from local system to Raspberry pi
   -Host name: IP address of Raspberry pi
   -Username and password entered
   -Hit Login Button
2. The winSCP is a FTP based system which is used to sed the files from the platform to the devicen
3. The device need some file like Iotivity 2.2.2 and some python scripts 
4. These files are transferred from the system to the device using Winscp
![](https://github.com/atifrizwan91/Greenhouse/blob/main/Images/2.PNG)

# Build and Install IoTivity on device
- [x] Open Putty and connect it with device (Raspberry pi)
1. Installed IoTivity version 2.2.2 from GitHub using
   ```git clone --recursive --depth 1 --single-branch --branch 2.2.2 https://github.com/iotivity/iotivity-lite.git iotivity-222```
2. Build and Run sample client and server
   - To build and run the sample execute the following commands. 
   - ``` ./build--server-lite.sh ```
   - ``` ./run-server-lite.sh```

![](https://github.com/atifrizwan91/Greenhouse/blob/main/Images/3.PNG)

<!-- Demo
Digital Twin Video Demo [Part 1](https://www.youtube.com/watch?v=QrcGZkdB7KY).

Digital Twin Video Demo [Part 2](https://www.youtube.com/watch?v=TILGCEQVeP8).-->

# Federated Learning

## FL server
  Run FL server form DT platform
  
## FL Clients
  Start FL clients from DT platform 
  
  ![]( https://github.com/atifrizwan91/DT-for-FL/blob/main/DT/DigitalTwin/Images/DT%20All.png)
  
# Overall Architecture of DT

 ![]( https://github.com/atifrizwan91/DT-for-FL/blob/main/DT/DigitalTwin/Images/Over%20All%20Architecture.png)
