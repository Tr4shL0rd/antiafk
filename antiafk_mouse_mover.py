"""moves the mouse every 60 seconds to prevent the machine going to sleep"""
#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple
from sys import argv
import sys
from time import sleep
import logging
import pyautogui
from pyautogui import Point

logging.basicConfig(
        filename="logs/mouse_mover.log",
        encoding="utf-8",
        format="[%(asctime)s]: %(message)s",
        level=logging.INFO
    )

DEBUG = False
try:
    if len(argv) >= 2:
        DEBUG = True
except IndexError:
    DEBUG = False

def split_xy(xy_pos: Point) -> Tuple[float, float]:
    """
    Split a tuple of x and y coordinates into separate variables.

    Parameters:
    ----------
    * xy `Point`: A tuple of x and y coordinates.

    Returns:
    -------
    * tuple: A tuple containing the separate x and y variables.

    Note:
    ----
    * Does the same as x,y = xy[0], xy[1]
    """

    return (xy_pos[0], xy_pos[1])


def is_near(xy_pos: Point, center_x: float, center_y: float, radius: int) -> bool:
    """
    Check if the position (x, y) is within a certain distance of the center position
    (center_x, center_y).

    Parameters:
    ----------
    * x        `int`: The x-coordinate of the position to check.
    * y        `int`: The y-coordinate of the position to check.
    * center_x `int`: The x-coordinate of the center position.
    * center_y `int`: The y-coordinate of the center position.
    * radius   `int`: The maximum distance from the center position that the position (x, y) is
        allowed to be.

    Returns:
    -------
    * bool: True if the distance between the two positions is less than or equal to the given
    radius, False otherwise.

    Note:
    ----
    * Created by OpenAI's ChatGPT AI
    """

    # Calculate the distance between the given position and the center position
    x_pos, y_pos = split_xy(xy_pos)
    distance = ((x_pos - center_x) ** 2 + (y_pos - center_y) ** 2) ** 0.5
    # Return whether the distance is less than or equal to the given radius
    return bool(distance <= radius)


def jiggle_mouse(xy_pos: Point) -> None:
    """
    Jiggle the mouse around the given position (x, y).

    Parameters:
    ----------
    * xy `tuple`: A tuple of x and y coordinates.

    Returns:
    ------
    * None
    """

    x_pos, y_pos = split_xy(xy_pos)
    pyautogui.moveTo(x_pos, y_pos + 1)


CENTER_LEFT = Point(1, 500)
SLEEP_TIME = 60 if not DEBUG else int(argv[1])
ORIGIN = pyautogui.position()

logging.info("STARTING at position %s |DEBUG = %s|SLEEP_TIME = %s|", ORIGIN, DEBUG, SLEEP_TIME)

def main() -> None:
    """main entry point of script"""
    pos = Point(pyautogui.position()[0], pyautogui.position()[1])
    pyautogui.moveTo(CENTER_LEFT)
    loop_num = 0
    while is_near(
        pos, CENTER_LEFT[0], CENTER_LEFT[1], radius=10
    ):  # checks if mouse is around CENTER_LEFT
        loop_num += 1
        jiggle_mouse(pos)
        for i in range(SLEEP_TIME, 0, -1):
            print(
                f"\rmoving mouse in {i} seconds"
                if i > 9
                else f"\rmoving mouse in 0{i} seconds",
                end="",
            )
            sleep(1)
        pyautogui.moveTo(pos)  # resets mouse pos
        logging.info("(LOOP #%s) MOVED TO %s", loop_num, split_xy(pos))
    print("stopped")
    logging.info("STOPPED by moving mouse")


try:
    if __name__ == "__main__":
        pyautogui.moveTo(CENTER_LEFT)
        main()
except KeyboardInterrupt:
    logging.info("STOPPED by KeyboardInterrupt")
    print("EXITING...")
    sys.exit()

except pyautogui.FailSafeException:
    logging.info("COULD NOT START! mouse in a corner")
    print("please move mouse away from corner!")
