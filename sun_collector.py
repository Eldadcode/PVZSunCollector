"""
File: sun_collector.py
Purpose: Automate the process of sun collection while playing Plants vs. Zombies
Author: Eldad Izhaky
Date: 21/10/2022
"""

import win32gui
import numpy as np
import pyautogui
import time
from typing import Tuple, List
from PIL import Image
import threading
import keyboard

SUN_COLOR = (0xFE, 0xF6, 0x01)
INDICES_AXIS = -1
SECONDS_TO_SLEEP_AFTER_COLLECTION = 0.1
PROGRAM_EXIT_KEY = 'K'


def get_color_coordinates_from_screenshot(screenshot: Image, color: Tuple[int, int, int]) -> List[Tuple[int, int]]:
    """
    This function returns a list of coordinates that contains the color in the given screenshot
    :param screenshot: the screenshot to find the color in
    :param color: the color to look for in the screenshot
    :return: a list of coordinates that contains the color in the given screenshot
    """

    image_array = np.array(screenshot)
    color_indices = np.where(np.all(image_array == color, axis=INDICES_AXIS))
    color_coordinations = list(zip(color_indices[0], color_indices[1]))
    return color_coordinations


def collect_sun(sun_coordination: Tuple[int, int]):
    """
    This function jumps to a sun on the screen, collects it and returns to the previous mouse position
    :param sun_coordination: the coordination of the sun to collect
    """

    # Get the location of the mouse to return the cursor to its original position after the sun collection
    current_mouse_x, current_mouse_y = win32gui.GetCursorPos()

    sun_x, sun_y = sun_coordination[1], sun_coordination[0]
    pyautogui.moveTo(sun_x, sun_y)
    pyautogui.leftClick()

    # Move the cursor back to its original location
    pyautogui.moveTo(current_mouse_x, current_mouse_y)


def sun_collector_loop():
    """
    Starts the loop of the sun collection.
    """

    while True:
        game_screenshot = pyautogui.screenshot()

        sun_coordinations = get_color_coordinates_from_screenshot(game_screenshot, SUN_COLOR)
        if sun_coordinations:
            collect_sun(sun_coordinations[0])
            time.sleep(SECONDS_TO_SLEEP_AFTER_COLLECTION)


def main():
    """
    The main function of the program. It starts a thread that collects the sun and stops the program after a key is pressed
    """

    sun_collector_thread = threading.Thread(target=sun_collector_loop)
    sun_collector_thread.daemon = True
    sun_collector_thread.start()

    while True:
        if keyboard.is_pressed(PROGRAM_EXIT_KEY):
            break


if __name__ == "__main__":
    main()
