import pyautogui
from pynput import keyboard
import time
from windows import get_window_center, is_within_bounds

# Get the window center coordinates (replace with your approach)
center_x, center_y = get_window_center()

# Ensure coordinates are retrieved before proceeding
if not (center_x and center_y):
    print("Window center not found. Exiting script.")
    exit()

# Move mouse to the center (optional click)
pyautogui.moveTo(center_x, center_y)


# Function to handle key press
def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        print("Loop terminated by pressing", key)
        listener.stop()
        print("Script stopped.")


# Create a global variable to control the loop
running = True

# Create the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Loop to wait for key presses (no continuous clicking)
while running:
    current_x, current_y = pyautogui.position()
    if is_within_bounds(current_x, current_y):
        pyautogui.click(center_x, center_y)
        # pyautogui.click(center_x + 5, center_y - 5)
        # pyautogui.click(center_x - 5, center_y + 5)
        # pyautogui.click(center_x + 10, center_y + 10)
        # pyautogui.click(center_x - 10, center_y - 10)
        time.sleep(0.01)  # Short wait to avoid busy waiting

# Stop the listener when the loop terminates
listener.stop()
print("Script stopped.")
