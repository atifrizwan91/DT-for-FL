# Setup Environment on Client
1. `curl https://pyenv.run | bash`
2. `sudo nano ~/.bashrc`

   Add the following three lines to the botton of the .bashrc file  
    `export PATH="$HOME/.pyenv/bin:$PATH"`   
     `eval "$(pyenv init --path)"`   
     `eval "$(pyenv virtualenv-init -)"`
3. `exec $SHELL`
4. `sudo apt-get install --yes libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libgdbm-dev lzma lzma-dev tcl-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev wget curl make build-essential openssl`
5. `pyenv update`
6. `pyenv install –list`
7. `pyenv install 3.8.0`   //Recommended version
8. `pyenv global 3.8.0`
9. `sudo apt update`
10. `sudo apt full-upgrade`
11. `mkdir project`
12. `cd project`
13. `python3 -m pip install virtualenv`
14. `python3 -m virtualenv env`     // env is environment name
15. `source env/bin/activate`
16. `sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev`
17. `pip install -U wheel mock six`

# Install Libraries
 `pip install Requirements.txt`

# Data Tranfer

1. Transfer this folder (Client) to IoT device using WinSCP FTP software

![](https://github.com/atifrizwan91/DT-for-FL/blob/main/DT/DigitalTwin/Images/FTP%20Client.png))

2. Install [IoTivity 2.2.2](http://iotivity.org/IoTivity-Getting-Started/). on IoT Device from [GitHub Repository](https://github.com/iotivity/iotivity-lite)
3. Start DT application of Client
```
python App.py
```
