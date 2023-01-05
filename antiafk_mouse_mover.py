#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple
from sys import argv
import pyautogui
from pyautogui import Point
from time import sleep
import datetime

DEBUG = False
try:
    if len(argv) >= 2:
        DEBUG = True
except IndexError:
    DEBUG = False


def get_current_time() -> str:
    """
    Get the current time in the format [HH:MM:SS | dd/mm/YYYY].

    Returns:
    -------
    * `str`: The current time in the specified format.

    Note:
    ----
    * Created by OpenAI's ChatGPT AI
    """

    # Get the current time
    time = datetime.datetime.now()
    # Format the time as a string in the desired format
    time_str = time.strftime("[%H:%M:%S | %d/%m/%Y]")
    return time_str


def split_xy(xy: Point) -> Tuple[float, float]:
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

    return (xy[0], xy[1])


def is_near(xy: Point, center_x: int, center_y: int, radius: int) -> bool:
    """
    Check if the position (x, y) is within a certain distance of the center position (center_x, center_y).

    Parameters:
    ----------
    * x        `int`: The x-coordinate of the position to check.
    * y        `int`: The y-coordinate of the position to check.
    * center_x `int`: The x-coordinate of the center position.
    * center_y `int`: The y-coordinate of the center position.
    * radius   `int`: The maximum distance from the center position that the position (x, y) is allowed to be.

    Returns:
    -------
    * bool: True if the distance between the two positions is less than or equal to the given radius, False otherwise.

    Note:
    ----
    * Created by OpenAI's ChatGPT AI
    """

    # Calculate the distance between the given position and the center position
    x, y = split_xy(xy)
    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
    # Return whether the distance is less than or equal to the given radius
    return bool(distance <= radius)


def jiggle_mouse(xy: Point) -> None:
    """
    Jiggle the mouse around the given position (x, y).

    Parameters:
    ----------
    * xy `tuple`: A tuple of x and y coordinates.

    Returns:
    ------
    * None
    """

    x, y = split_xy(xy)
    pyautogui.moveTo(x, y + 1)


CENTER_LEFT = (1, 500)
SLEEP_TIME = 60 if not DEBUG else int(argv[1])
ORIGIN = pyautogui.position()
with open("logs/mouse_mover.log", "a") as f:
    f.write(
        f"{get_current_time()}: STARTING at position {ORIGIN} |{DEBUG = }|{SLEEP_TIME = }|\n"
    )


def main() -> None:
    pos = Point(pyautogui.position()[0], pyautogui.position()[1])
    pyautogui.moveTo(CENTER_LEFT)
    while is_near(
        pos, CENTER_LEFT[0], CENTER_LEFT[1], radius=10
    ):  # checks if mouse is around CENTER_LEFT
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
        with open("logs/mouse_mover.log", "a") as f:
            f.write(f"{get_current_time()}: MOVED TO {split_xy(pos)}\n")
    print("stopped")
    with open("logs/mouse_mover.log", "a") as f:
        f.write(f"{get_current_time()}: STOPPED by moving mouse\n")


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    with open("logs/mouse_mover.log", "a") as f:
        f.write(f"{get_current_time()}: STOPPED by KeyboardInterrut\n")
    print("EXITING...")
    exit()

except pyautogui.FailSafeException:
    with open("logs/mouse_mover.log", "a") as f:
        f.write(f"{get_current_time()}: COULD NOT START! mouse in a corner\n")
    print("please move mouse away from corner!")
