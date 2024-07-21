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

# Create a global variable to control the loop
running = True

# Global flag to control auto mode
auto_mode = True

# global flag to decide shoot left or right
shoot_left = True

# shoot duration for left / right side
shoot_duration = 0.75


# Method to handle shoot left and right
def shoot_left_right(left: bool):
    if left:
        cur_x, cur_y = pyautogui.position()
        if is_within_bounds(cur_x, cur_y):
            current_shoot_time = time.time()
            end_time = time.time() + shoot_duration
            _first_time = True
            while current_shoot_time < end_time:
                if auto_mode:
                    if _first_time:
                        pyautogui.mouseDown(center_x, center_y)
                        pyautogui.moveTo(center_x - 100, center_y)
                        pyautogui.mouseUp()
                    else:
                        pyautogui.click(center_x, center_y)
                    current_shoot_time = time.time()
                    _first_time = False
                else:
                    return True
            return False
    else:
        cur_x, cur_y = pyautogui.position()
        if is_within_bounds(cur_x, cur_y):
            current_shoot_time = time.time()
            end_time = time.time() + shoot_duration
            _first_time = True
            while current_shoot_time < end_time:
                if auto_mode:
                    if _first_time:
                        pyautogui.mouseDown(center_x, center_y)
                        pyautogui.moveTo(center_x + 100, center_y)
                        pyautogui.mouseUp()
                    else:
                        pyautogui.click(center_x, center_y)
                    current_shoot_time = time.time()
                    _first_time = False
                else:
                    return False
            return True

    return False


# Function to handle key press
def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        print("Loop terminated by pressing", key)
        listener.stop()
        print("Script stopped.")
    elif key == keyboard.Key.left:
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x - 100, center_y)
            pyautogui.mouseUp()

    elif key == keyboard.Key.right:
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x + 100, center_y)
            pyautogui.mouseUp()

    elif key == keyboard.Key.space:
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            pyautogui.click(center_x, center_y)

    elif key == keyboard.Key.up:
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            pyautogui.mouseDown(center_x, center_y + 25)
            pyautogui.moveTo(center_x, center_y - 50)
            pyautogui.mouseUp()
    elif key == keyboard.Key.ctrl_l:
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            pyautogui.mouseDown(center_x + 100, center_y + 75)
            pyautogui.moveTo(center_x - 150, center_y - 200)
            pyautogui.mouseUp()
    elif key == keyboard.Key.alt_l:
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            pyautogui.mouseDown(center_x - 100, center_y + 75)
            pyautogui.moveTo(center_x + 150, center_y - 200)
            pyautogui.mouseUp()
    elif key == keyboard.Key.shift:
        global auto_mode
        current_x, current_y = pyautogui.position()
        if is_within_bounds(current_x, current_y):
            auto_mode = not auto_mode


# Create the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Loop to wait for key presses (no continuous clicking)
while running:
    shoot_left = shoot_left_right(shoot_left)
    time.sleep(0.1)  # Short wait to avoid busy waiting

# Stop the listener when the loop terminates
listener.stop()
print("Script stopped.")
