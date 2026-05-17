import pyautogui
import pyperclip
import time
import webbrowser

# Open browser
webbrowser.open("https://www.google.com")
pyautogui.hotkey("ctrl", "alt", "b")  # or use Windows key
time.sleep(2)

# Open Chrome using Windows search
pyautogui.hotkey("win", "s")
time.sleep(1)
pyautogui.hotkey("ctrl", "v")
time.sleep(1)
pyautogui.press("enter")
time.sleep(3)

# Click address bar
pyautogui.click(700, 50)  # adjust coordinates
time.sleep(1)

# Type search query
pyperclip.copy("recent match score")
pyautogui.hotkey("ctrl", "v")
time.sleep(1)
pyautogui.press("enter")
time.sleep(3)

# Click first link
pyautogui.click(700, 300)  # adjust coordinates
time.sleep(2)

print("Done!")