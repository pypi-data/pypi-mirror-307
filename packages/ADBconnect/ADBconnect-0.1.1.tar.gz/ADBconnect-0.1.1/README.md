# ADBconnect  
**Control your phone from your PC via USB debugging.**

### Installation:  
Before using ADBconnect, you need to install [ADB](https://developer.android.com/tools/releases/platform-tools?hl=ru).  

### Setup:
#### USB:  
To configure the device you can use arguments:  
```commandline
adb_path - path to adb
device - ID of the device to connect (if you don’t specify it, it will try to connect to the first existing one)
name - device name
``` 
<br>

```python
from ADBconnect import USB

phone = USB(adb_path=r"C:\Users\ijidishurka\platform-tools", device='67e345rf')

phone.action.tap(100, 100)
```
in order to find out the device ID, enter adb devices

<br>

#### WIFI:  
```commandline
*ip - device ip address
adb_path - path to adb
port - device port (default 5555)
name - device name
``` 
<br>

```python
from ADBconnect import WIFI

phone = WIFI(adb_path=r"C:\Users\ijidishurka\platform-tools", ip='192.168.0.101')

phone.action.tap(100, 100)
```

### See code examples on our [github](https://github.com/Ijidishurka/ADBconnect/tree/main/examples)