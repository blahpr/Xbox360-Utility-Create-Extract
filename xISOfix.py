import pyautogui
import time
import subprocess

# Start the program without a console window
subprocess.Popen([r'x_tool\360 mp Gui v1.5.0.0\360mpGui v1.5.0.0.exe'], creationflags=subprocess.CREATE_NO_WINDOW)

# Wait for the program to load
time.sleep(4.5)

# Simulate mouse clicks and keystrokes
pyautogui.click(x=1060, y=608)  # Click OK on Error Message About no Drive Detected
pyautogui.press('enter')        # Press Enter Key
pyautogui.click(x=843, y=361)   # Click Create ISO Tab
pyautogui.click(x=982, y=702)   # Click Convert an created ISO Button
