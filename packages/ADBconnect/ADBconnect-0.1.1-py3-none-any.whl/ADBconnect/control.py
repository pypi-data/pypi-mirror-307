# -*- coding: utf-8 -*-
import time


class Control:
    def __init__(self, commander):
        self._adb_command = commander.adb_command

    def get_device_info(self) -> dict:
        """Retrieves detailed information about the device."""
        device_info = {
            "Model": self._adb_command('shell getprop ro.product.model').strip(),
            "Android Version": self._adb_command('shell getprop ro.build.version.release').strip(),
            "SDK Version": self._adb_command('shell getprop ro.build.version.sdk').strip(),
            "Device": self._adb_command('shell getprop ro.product.device').strip(),
            "Manufacturer": self._adb_command('shell getprop ro.product.manufacturer').strip(),
            "Board": self._adb_command('shell getprop ro.product.board').strip(),
            "Hardware": self._adb_command('shell getprop ro.product.hardware').strip(),
            "Serial": self._adb_command('shell getprop ro.serialno').strip(),
            "Build ID": self._adb_command('shell getprop ro.build.display.id').strip(),
            "Fingerprint": self._adb_command('shell getprop ro.build.fingerprint').strip(),
            "Host": self._adb_command('shell getprop ro.build.host').strip(),
            "Time": self._adb_command('shell getprop ro.build.date').strip(),
        }
        return device_info
    
    def get_apps(self) -> list:
        """Gets a list of installed applications on the device.
        :return: List of applications
        """
        
        result = self._adb_command("shell pm list packages -3")
        return [line.replace('package:', '').strip() for line in result.splitlines() if line]
    
    def run_app(self, package_name: str):
        """Launches an application by package name.
        :return: class for application control
        """
        app = Application(package_name, self._adb_command)
        app.launch()
        return app
    
    def stop_app(self, package_name) -> None:
        """Stops an application by package name."""
        self._adb_command(f"shell am force-stop {package_name}")
        
        
class Application:
    def __init__(self, package_name, adb_command):
        self.package_name = package_name
        self._adb_command = adb_command

    def launch(self) -> None:
        """Launches an application"""
        self._adb_command(f"shell monkey -p {self.package_name} -c android.intent.category.LAUNCHER 1")
        
    def close(self) -> None:
        """Stops the application."""
        self._adb_command(f"shell am force-stop {self.package_name}")
        
    def restart(self) -> None:
        """Reloads the application."""
        self.close()
        time.sleep(1)
        self.launch()

    def __repr__(self):
        return f"Application(package_name='{self.package_name}')"