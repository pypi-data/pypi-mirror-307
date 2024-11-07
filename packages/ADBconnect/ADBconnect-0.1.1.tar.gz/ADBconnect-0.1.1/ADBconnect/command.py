import subprocess


class Commander:
    def __init__(self, adb_path, device, name):
        self.adb_path = adb_path
        self.device = device
        self.name = name

    def adb_command(self, command, shell=True, capture_output=True, text=True) -> str:
        """Method for executing an ADB command and returning the result."""
        
        if not self.device:
            result = subprocess.run(f"adb {command}", shell=shell, capture_output=capture_output, text=text)
        else:
            result = subprocess.run(f"adb -s {self.device} {command}", shell=shell, capture_output=capture_output, text=text)
            
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise RuntimeError(f"ADB command failed: {result.stderr.strip()}")