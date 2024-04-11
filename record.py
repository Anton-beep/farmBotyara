from pynput import keyboard, mouse
import time
import json

keyboard_events = []
mouse_events = []
start_time = time.time()


def on_press(key):
    current_time = time.time() - start_time
    if key == keyboard.Key.esc:
        keyboard_events.append(('key_press', 'esc', current_time))
    else:
        try:
            keyboard_events.append(('key_press', key.char, current_time))
        except AttributeError:
            keyboard_events.append(('key_press', str(key), current_time))


def on_release(key):
    current_time = time.time() - start_time
    if key == keyboard.Key.esc:
        keyboard_events.append(('key_release', 'esc', current_time))
        return False  # Stop listener
    else:
        try:
            keyboard_events.append(('key_release', key.char, current_time))
        except AttributeError:
            keyboard_events.append(('key_release', str(key), current_time))


last_x, last_y = None, None
distance_threshold = 10  # Change this to adjust the sensitivity


def on_move(x, y):
    global last_x, last_y
    current_time = time.time() - start_time
    if last_x is None and last_y is None:
        last_x, last_y = x, y
        mouse_events.append(('move', x, y, current_time))
    else:
        distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
        if distance > distance_threshold:
            last_x, last_y = x, y
            mouse_events.append(('move', x, y, current_time))


def on_click(x, y, button, pressed):
    current_time = time.time() - start_time
    action = 'press' if pressed else 'release'
    # Convert button to a string that can be serialized
    button_str = str(button)
    mouse_events.append((action, x, y, button_str, current_time))
    if button == mouse.Button.middle:  # Use middle button to stop recording
        return False


def on_scroll(x, y, dx, dy):
    current_time = time.time() - start_time
    # Convert dx, dy to string if needed or serialize directly
    mouse_events.append(('scroll', x, y, dx, dy, current_time))


# Record keyboard and mouse events
with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
        mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as m_listener:
    k_listener.join()
    m_listener.join()

# Save events to file
with open('keyboard_events.json', 'w') as f:
    json.dump(keyboard_events, f)
with open('mouse_events.json', 'w') as f:
    json.dump(mouse_events, f)
