import pyautogui
import time

# Mouse functions
print(pyautogui.size())  # Prints the resolution of your screen
time.sleep(3)
print(pyautogui.position())  # Prints the current position of the mouse

# Moves the mouse over time
pyautogui.moveTo(100, 100, 5)

# Move the mouse relative to its current position
pyautogui.moveRel(100, 100, 3)

# Click
pyautogui.click(100, 100, 3, 3, button="left")
pyautogui.rightClick()
pyautogui.leftClick()
