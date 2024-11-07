# -*- coding: utf-8 -*-

class Servis:
	def __init__(self, commander):
		self._adb_command = commander.adb_command
		
	def wifi(self, enable: bool) -> None:
		"""Turns Wi-Fi on or off."""
		if enable:
			self._adb_command("shell svc wifi enable")
		else:
			self._adb_command("shell svc wifi disable")
		
	def set_proxy(self, ip: str, port: int) -> None:
		"""enable proxy for phone
		:param ip: Proxy server ip address.
		:param port: Server proxy port.
		"""
		self._adb_command(f"shell settings put global http_proxy {ip}:{port}")
		
	def reset_proxy(self) -> None:
		"""reset proxy settings"""
		self._adb_command(f"shell settings put global http_proxy :0")
	
	def bluetooth(self, enable: bool) -> None:
		"""Turns Bluetooth on or off."""
		if enable:
			self._adb_command("shell service call bluetooth_manager 6")
		else:
			self._adb_command("shell service call bluetooth_manager 8")
	
	def airplane_mode(self, enable: bool) -> None:
		"""Turns airplane mode on or off."""
		if enable:
			self._adb_command("shell settings put global airplane_mode_on 1")
			self._adb_command("shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true")
		else:
			self._adb_command("shell settings put global airplane_mode_on 0")
			self._adb_command("shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false")
	
	def mobile_data(self, enable: bool) -> None:
		"""Disables mobile network data transmission on the device."""
		if enable:
			self._adb_command("shell svc data enable")
		else:
			self._adb_command("shell svc data disable")