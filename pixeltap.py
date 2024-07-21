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
        try:
            # Replace 'path/to/circle_image.png' with the actual path to your circle image
            circle_image = pyautogui.locateOnScreen("circle_pink.png", grayscale=True)

            if circle_image is None:
                print("Circle not found on screen.")
            else:
                # Get the coordinates of the top left corner of the circle image
                x, y = circle_image

                # Get the width and height of the circle image (assuming it's a square)
                width = circle_image.width
                height = circle_image.height

                # Calculate the center coordinates of the circle image
                image_center_x = x + width // 2
                image_center_y = y + height // 2

                # Click on the center of the circle
                pyautogui.click(image_center_x, image_center_y)
                print(f"Clicked on the center of the circle at coordinates: ({image_center_x}, {image_center_y})")

                time.sleep(0.01)
        except pyautogui.ImageNotFoundException:
            print("Image not found on the screen.")

# Stop the listener when the loop terminates
listener.stop()
print("Script stopped.")
