import shutil
import os
import time

from .command import Commander
from .control import Control
from .screen import Screen
from .action import Action
from .servis import Servis

adbu = 'https://developer.android.com/tools/releases/platform-tools'


class USB:
    def __init__(self, adb_path=None, device=None, name='phone'):
        if adb_path:
            os.environ['PATH'] += os.pathsep + adb_path

        if not shutil.which("adb"):
            raise EnvironmentError(f"ADB not found. Make sure ADB is installed and added to PATH. Download adb - {adbu}")
        
        self.config = Commander(adb_path, device, name)
        
        if not device:
            devices = self.config.adb_command('devices')
            print(devices)
        
        self.config.adb_command('shell getprop ro.product.model')
        
        self.action = Action(self.config)
        self.servis = Servis(self.config)
        
        self.screen = Screen(self.config)
        self.control = Control(self.config)


class WIFI:
    def __init__(self, ip: str, port=5555, adb_path=None, name='phone'):
        if adb_path:
            os.environ['PATH'] += os.pathsep + adb_path
        
        if not shutil.which("adb"):
            raise EnvironmentError(f"ADB not found. Make sure ADB is installed and added to PATH. Download adb - {adbu}")
        
        self.config = Commander(adb_path, f'{ip}:{port}', name)
        
        self.config.adb_command(f'tcpip {port}')
        time.sleep(1)
        self.config.adb_command(f'connect {ip}:{port}')

        self.action = Action(self.config)
        self.servis = Servis(self.config)
        
        self.screen = Screen(self.config)
        self.control = Control(self.config)
        

__all__ = ["USB", "WIFI"]