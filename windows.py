import win32gui

# Replace with the exact title of the window you want
window_title = "Telegram"


def get_window_center():
    hwnd = win32gui.FindWindow(None, window_title)  # Find the window handle
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # Get window position
        width = right - left
        height = bottom - top
        c_x = left + (width // 2)  # Calculate center coordinates
        c_y = top + (height // 2)
        return c_x, c_y
    else:
        print("Window not found")
        return None


def is_within_bounds(x, y):
    hwnd = win32gui.FindWindow(None, window_title)  # Find the window handle
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # Get window position
        # Check if the point is within the window rectangle
        return left <= x <= right and top <= y <= bottom
    else:
        print("Window not found")
        return False


def window_region():
    hwnd = win32gui.FindWindow(None, window_title)  # Find the window handle
    if hwnd:
        left, top, width, height = win32gui.GetWindowRect(hwnd)  # Get window position
        # Check if the point is within the window rectangle
        return left, top, width, height
    else:
        print("Window not found")
        return None
