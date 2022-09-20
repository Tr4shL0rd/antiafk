import pyautogui
from time import sleep

pyautogui.moveTo(1,500)
while pyautogui.position() == (1,500) or pyautogui.position() == (1,501):
    pyautogui.moveTo(1,500)
    sleep(59)
    pyautogui.moveTo(1,501)
print("stopped")
exit()
