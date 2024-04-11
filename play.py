import json
import time
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from threading import Thread

keyboard_controller = KeyboardController()
mouse_controller = MouseController()

# Load events from file
with open('keyboard_events.json', 'r') as f:
    keyboard_events = json.load(f)
with open('mouse_events.json', 'r') as f:
    mouse_events = json.load(f)


def play_keyboard_events():
    last_time = 0
    for event in keyboard_events:
        event_type, key, event_time = event
        time.sleep(event_time - last_time)  # Delay to match the recorded timing
        last_time = event_time
        if event_type == 'key_press':
            try:
                keyboard_controller.press(key)
            except ValueError:
                keyboard_controller.press(getattr(Key, key))
        elif event_type == 'key_release':
            try:
                keyboard_controller.release(key)
            except ValueError:
                keyboard_controller.release(getattr(Key, key))


def play_mouse_events():
    last_time = 0
    for event in mouse_events:
        action, *args, event_time = event
        time.sleep(event_time - last_time)
        last_time = event_time
        if action == 'move':
            x, y = args
            mouse_controller.position = (x, y)
        elif action in ['press', 'release']:
            x, y, button_str = args
            # Remove the "Button." prefix and convert the remaining part back to a Button object
            button = getattr(Button, button_str.split('.')[1].lower())
            mouse_controller.position = (x, y)
            if action == 'press':
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)
        elif action == 'scroll':
            x, y, dx, dy = args
            mouse_controller.position = (x, y)
            mouse_controller.scroll(dx, dy)


# Threads for playing back keyboard and mouse events simultaneously
keyboard_thread = Thread(target=play_keyboard_events)
mouse_thread = Thread(target=play_mouse_events)

keyboard_thread.start()
mouse_thread.start()

keyboard_thread.join()
mouse_thread.join()
