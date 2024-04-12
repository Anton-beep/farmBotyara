from modules.keyboard import Keyboard
from modules.mouse import Mouse

import json
import time
import win32api
import win32con

mouse = Mouse(800)
keyboard = Keyboard()
keyboard.release_all_keys()
mouse.up_left()
mouse.up_right()


def playback_events():
    with open('events.json', 'r') as f:
        events = json.load(f)

    last_time = 0
    for event in events:
        event_type, *args = event
        current_time = args[-1]
        time.sleep(current_time - last_time)
        last_time = current_time

        if event_type == 'move':
            x, y = args[0], args[1]
            mouse.move_relative(x, y)
        elif event_type == 'click':
            x, y, button, pressed = args[0], args[1], args[2], args[3]
            if pressed:
                if 'Button.left' in button:
                    mouse.down_left()
                elif 'Button.right' in button:
                    mouse.down_right()
            else:
                if 'Button.left' in button:
                    mouse.up_left()
                elif 'Button.right' in button:
                    mouse.up_right()

        elif event_type == 'scroll':
            x, y, dx, dy = args[0], args[1], args[2], args[3]
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, dy, 0)

        elif event_type in ['keypress', 'keyrelease']:
            key = args[0]
            if event_type == 'keypress':
                keyboard.press_key(key)
            elif event_type == 'keyrelease':
                keyboard.release_key(key)

    keyboard.release_all_keys()


time.sleep(1)
mouse.move_to_center()
time.sleep(1)
playback_events()
