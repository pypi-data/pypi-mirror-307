# -*- coding: utf-8 -*-
import time
import cv2
import os
import numpy as np


class Screen:
    def __init__(self, commander):
        self._adb_command = commander.adb_command
        
    def screenshot(self, filename="screen.png") -> str:
        """Takes a screenshot and saves it to disk."""
        self._adb_command("exec-out screencap -p > {}".format(filename))
        return filename
    
    def search_image(self, image_file, attempts=1, wait_time=0) -> tuple:
        """
        Searches for an image on the screen, taking several screenshots.
    
        :param image_file: Name of the image file to search for.
        :param attempts: Number of search attempts.
        :param wait_time: Time in seconds between attempts.
        :return: Coordinates of the found image or None if not found.
        """
    
        if not os.path.isfile(image_file):
            raise FileNotFoundError(f"Файл {image_file} не найден.")
        
        for attempt in range(attempts):
            screenshot_path = self.screenshot('find.png')
            coordinates = self._find_image(screenshot_path, image_file)
            os.remove('find.png')
        
            if coordinates:
                return coordinates[0]
        
            time.sleep(wait_time)
    
        return ()
        
    def _find_image(self, screenshot_path, image_path):
        screenshot = cv2.imread(screenshot_path)
        image = cv2.imread(image_path)
    
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        result = cv2.matchTemplate(screenshot_gray, image_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)
    
        points = []
        h, w = image_gray.shape
    
        for pt in zip(*locations[::-1]):
            center_x = pt[0] + w // 2
            center_y = pt[1] + h // 2
            points.append((center_x, center_y))
    
        return points