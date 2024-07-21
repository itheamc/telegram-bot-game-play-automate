import pyautogui
from pynput import keyboard
import time
from windows import get_window_center, is_within_bounds, window_region

# Images
home_play_btn_image = "images/play-button.png"
loading_game_image = "images/loading-game.png"
leave_the_city_btn_image = "images/leave-the-city-button.png"
gameplay_image = "images/exit-button.png"
leave_game_btn_image = "images/leave-button.png"
return_on_game_btn_image = "images/return-button.png"
wave_2_image = "images/wave-2.png"
wave_3_image = "images/wave-3.png"
wave_5_image = "images/wave-5.png"
wave_9_image = "images/wave-9.png"
wave_14_image = "images/wave-5.png"
wave_15_image = "images/wave-9.png"

# Get the window center coordinates (replace with your approach)
center_x, center_y = get_window_center()

# telegram window region
telegram_window_region = window_region()

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

# Game Start Time
game_start_time = None

# global flag to decide shoot left or right
shoot_left = True

# shoot duration for left / right side
shoot_duration = 0.75

# threshold for moving left or right
# in seconds
move_in_each_step_threshold = 1

# current move direction
DIRECTION_LEFT = 'left_direction'
DIRECTION_RIGHT = 'right_direction'
current_moving_direction = DIRECTION_LEFT

# current moving step count
MAX_MOVING_STEP = 15
current_moving_step = 0


# Method to find centers
def find_center(rect):
    left, top, width, height = rect
    cx = left + width / 2
    cy = top + height / 2
    return cx, cy


# Method to jump
def jump():
    current_x, current_y = pyautogui.position()
    if is_within_bounds(current_x, current_y):
        pyautogui.mouseDown(center_x, center_y + 25)
        pyautogui.moveTo(center_x, center_y - 50)
        pyautogui.mouseUp()


# Method to handle shoot left and right
def shoot_left_right(left: bool):
    if left:
        cur_x, cur_y = pyautogui.position()
        if is_within_bounds(cur_x, cur_y):
            current_shoot_time = time.time()
            end_time = time.time() + shoot_duration
            _first_time = True
            # _count = 0
            while current_shoot_time < end_time:
                if auto_mode:
                    if _first_time:
                        pyautogui.mouseDown(center_x, center_y)
                        pyautogui.moveTo(center_x - 100, center_y)
                        pyautogui.mouseUp()
                    else:
                        # if _count == 3:
                        #     if is_in_wave(5) or is_in_wave(9) or is_in_wave(14):
                        #         jump()
                        #     else:
                        #         pyautogui.click(center_x, center_y)
                        # else:
                        #     pyautogui.click(center_x, center_y)
                        pyautogui.click(center_x, center_y)
                    current_shoot_time = time.time()
                    _first_time = False
                    # _count += 1
                else:
                    return True
            return False
    else:
        cur_x, cur_y = pyautogui.position()
        if is_within_bounds(cur_x, cur_y):
            current_shoot_time = time.time()
            end_time = time.time() + shoot_duration
            _first_time = True
            # _count = 0
            while current_shoot_time < end_time:
                if auto_mode:
                    if _first_time:
                        pyautogui.mouseDown(center_x, center_y)
                        pyautogui.moveTo(center_x + 100, center_y)
                        pyautogui.mouseUp()
                    else:
                        # if _count == 2:
                        #     if is_in_wave(3) or is_in_wave(9) or is_in_wave(14):
                        #         jump()
                        #     else:
                        #         pyautogui.click(center_x, center_y)
                        # else:
                        #     pyautogui.click(center_x, center_y)
                        pyautogui.click(center_x, center_y)
                    current_shoot_time = time.time()
                    _first_time = False
                    # _count += 1
                else:
                    return False
            return True

    return False


# method to handle move left or right
def move_left_or_right(direction):
    global current_moving_step
    if direction == DIRECTION_LEFT:
        __take_medikit()
        current_moving_step = 0
        if not shoot_left:
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x - 100, center_y)
            pyautogui.mouseUp()

        while current_moving_step < MAX_MOVING_STEP:
            if not running or not auto_mode or not is_game_running():
                break
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x - 100, center_y, duration=move_in_each_step_threshold)
            __shoot_now(DIRECTION_RIGHT)

            __shoot_now()
            current_moving_step += 1

        return DIRECTION_RIGHT
    else:
        __take_medikit()
        current_moving_step = 0
        if shoot_left:
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x + 100, center_y)
            pyautogui.mouseUp()

        while current_moving_step < MAX_MOVING_STEP:
            if not running or not auto_mode or not is_game_running():
                break
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x + 100, center_y, duration=move_in_each_step_threshold)
            __shoot_now(DIRECTION_LEFT)

            __shoot_now()
            current_moving_step += 1

        return DIRECTION_LEFT


# Method to shoot
def __shoot_now(direction=None, turn_after_shoot=True):
    if direction:
        if direction == DIRECTION_LEFT:
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x - 100, center_y)
            pyautogui.mouseUp()
        else:
            if direction == DIRECTION_RIGHT:
                pyautogui.mouseDown(center_x, center_y)
                pyautogui.moveTo(center_x + 100, center_y)
                pyautogui.mouseUp()

    _start_time = time.time()
    _end_time = time.time() + shoot_duration
    while _start_time < _end_time:
        if not running or not auto_mode:
            return
        pyautogui.click(center_x, center_y)
        _start_time = time.time()

    if direction and turn_after_shoot:
        if direction == DIRECTION_LEFT:
            pyautogui.mouseDown(center_x, center_y)
            pyautogui.moveTo(center_x + 100, center_y)
            pyautogui.mouseUp()
        else:
            if direction == DIRECTION_RIGHT:
                pyautogui.mouseDown(center_x, center_y)
                pyautogui.moveTo(center_x - 100, center_y)
                pyautogui.mouseUp()


# Method to take medikit
def __take_medikit():
    _l, _t, _w, _h = telegram_window_region
    pyautogui.click(_w - 60, _h - 80)


# Method to get the play game button position
def play_game_button_position():
    try:
        location = pyautogui.locateOnScreen(home_play_btn_image, region=telegram_window_region)
        return location.left, location.top, location.width, location.height
    except pyautogui.ImageNotFoundException:
        return None


# Method to check if game is loading
def is_game_loading():
    try:
        location = pyautogui.locateOnScreen(loading_game_image, region=telegram_window_region)
        return location is not None
    except pyautogui.ImageNotFoundException:
        return False


# Method to get leave the city button position
def leave_the_city_button_position():
    try:
        location = pyautogui.locateOnScreen(leave_the_city_btn_image, region=telegram_window_region)
        return location.left, location.top, location.width, location.height
    except pyautogui.ImageNotFoundException:
        return None


# Method to check if game is running
def is_game_running():
    try:
        _l, _t, _w, _h = telegram_window_region
        _region = (_w - 200, _t + 100, 200, 200)
        pyautogui.locateOnScreen(gameplay_image, region=_region)
        return True
    except pyautogui.ImageNotFoundException:
        return False


# Method to get leave button position
def leave_button_position():
    try:
        location = pyautogui.locateOnScreen(leave_game_btn_image, region=telegram_window_region)
        return location.left, location.top, location.width, location.height
    except pyautogui.ImageNotFoundException:
        return None


# Method to get return on game button position
def return_on_game_button_position():
    try:
        location = pyautogui.locateOnScreen(return_on_game_btn_image, region=telegram_window_region)
        return location.left, location.top, location.width, location.height
    except pyautogui.ImageNotFoundException:
        return None


# Method to check if game is in given wave
def is_in_wave(wave: int):
    try:
        _waves_images = {
            2: wave_2_image,
            3: wave_3_image,
            5: wave_5_image,
            9: wave_9_image,
            14: wave_14_image,
            15: wave_15_image
        }

        _image = _waves_images.get(wave)

        if _image:
            _l, _t, _w, _h = telegram_window_region
            _region = (_l + 20, _t + 20, _w - 20, 250)
            location = pyautogui.locateOnScreen(_image, region=_region, grayscale=True)

            print('location', location)

            return location is not None
        return False
    except pyautogui.ImageNotFoundException:
        return False


# method for formatted print
def _print_this(message):
    print(f'\U0001F449 \U0001F449 \U0001F449 {message} \U0001F448 \U0001F448 \U0001F448')


# Function to handle key press
def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        print("Loop terminated by pressing", key)
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

# NOTAI not found count and threshold
NOTAI_NOT_FOUND_EXIT_THRESHOLD = 10
notai_not_found_count = 0

# Total game played
total_game_played = 0

# Loop to wait for key presses (no continuous clicking)
while running:
    _game_running = is_game_running()
    if _game_running:
        if game_start_time is None:
            _print_this("PLAYING")
            game_start_time = time.time()
            notai_not_found_count = 0
            total_game_played += 1

        # shoot_left = shoot_left_right(shoot_left)
        current_moving_direction = move_left_or_right(current_moving_direction)
        time.sleep(0.1)  # Short wait to avoid busy waiting
    else:
        play_btn_pos = play_game_button_position()
        if play_btn_pos:
            _print_this("PRESSING START BUTTON")
            x, y = find_center(play_btn_pos)
            pyautogui.click(x, y)
            time.sleep(2)
        else:
            _loading = is_game_loading()
            if _loading:
                _print_this("LOADING")
                time.sleep(1)
            else:
                leave_the_city_btn_pos = leave_the_city_button_position()
                if leave_the_city_btn_pos:
                    _print_this("LEAVING THE CITY")
                    x, y = find_center(leave_the_city_btn_pos)
                    pyautogui.click(x, y)
                    time.sleep(2)
                else:
                    # leave_btn_pos = leave_button_position()
                    return_btn_pos = return_on_game_button_position()
                    if return_btn_pos:
                        _print_this(
                            f"LEAVING GAME ({(time.time() - game_start_time).__int__() if game_start_time is not None else 0} sec)")
                        _print_this(f'Total game played: {total_game_played}')
                        x, y = find_center(return_btn_pos)
                        pyautogui.click(x, y)
                        auto_mode = True
                        game_start_time = None
                        time.sleep(2)
                    else:
                        notai_not_found_count += 1
                        time.sleep(1)
                        _print_this(f"NOTAI not found. Retried {notai_not_found_count}")
                        if NOTAI_NOT_FOUND_EXIT_THRESHOLD == notai_not_found_count:
                            running = False

# Stop the listener when the loop terminates
listener.stop()
print("Script stopped.")
