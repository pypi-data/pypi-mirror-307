# -*- coding: utf-8 -*-

class Action:
	def __init__(self, commander):
		self._adb_command = commander.adb_command

	def tap(self, x: int, y: int) -> None:
		"""Clicks on the screen at the specified coordinates."""
		self._adb_command(f"shell input tap {x} {y}")
	
	def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration=999) -> None:
		"""swipe from one place to another."""
		self._adb_command(f"shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}")
		
	def input_text(self, text: str) -> None:
		"""Enter some message into the text field for input."""
		self._adb_command(f'shell input text "{text.replace(" ", "%s")}"')
		
	def screen(self) -> None:
		"""Turns phone screen on or off."""
		self._adb_command("shell input keyevent 26")
	
	def reboot(self) -> None:
		"""Reboot phone."""
		self._adb_command("shell reboot")
		
	def power_off(self) -> None:
		"""Reboot phone."""
		self._adb_command("shell reboot -p")
		
	def toast(self, message: str) -> None:
		"""Display a message on the screen."""
		self._adb_command(f'shell settings put global toast "{message}"')
		
	def send_notification(self, text):
		"""Sends a notification to the device with the specified text."""
		command = f'shell cmd notification post default_channel {text}'
		self._adb_command(command)
		
	def set_brightness(self, value: int) -> None:
		"""Sets the screen brightness (from 0 to 255)."""
		if 0 <= value <= 255:
			self._adb_command(f'shell settings put system screen_brightness {value}')
		else:
			raise ValueError("Brightness should be between 0 and 255.")
		
	def set_volume(self, volume: int) -> None:
		"""Sets the sound level (from 0 to 15)."""
		if 0 <= volume <= 15:
			self._adb_command(f'shell media volume --set {volume}')
		else:
			raise ValueError("The sound level should be between 0 and 15.")