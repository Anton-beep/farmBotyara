from modules.mouse import Mouse
from pynput import mouse, keyboard
import time
import json

mouse_move = []
key_down = []
key_up = []

COEF = 1

mouse_ = Mouse(800)

movements = []
pressed_keys = {}
BUFFER_X = 0
BUFFER_Y = 0


def on_move(*args):
    global start_time, last_x, last_y, movements, BUFFER_X, BUFFER_Y
    x, y = mouse_.get_pos()
    dx, dy = int(x - last_x), int(y - last_y)

    if abs(dx) > mouse_.x_size * 0.1 or abs(dy) > mouse_.y_size * 0.1:
        pass
    else:
        if abs(dx) > 15 or abs(dy) > 15:
            mouse_move.append(('move', dx, dy, time.time() - start_time))
            last_x, last_y = x, y


def on_click(x, y, button, pressed):
    mouse_move.append(('click', 0, 0, str(button), pressed, time.time() - start_time))


def on_scroll(x, y, dx, dy):
    mouse_move.append(('scroll', x, y, dx, dy, time.time() - start_time))


def on_press(key):
    key = str(key).replace("'", "")
    if key in pressed_keys.keys():
        if pressed_keys[key]:
            pass
        else:
            key_down.append((key, time.time() - start_time))
            pressed_keys[key] = True
    else:
        key_down.append((key, time.time() - start_time))
        pressed_keys.update({key: True})


def on_release(key):
    key = str(key).replace("'", "")
    key_up.append((key, time.time() - start_time))
    pressed_keys[key] = False
    if key == "Key.esc":
        return False  # Stop listener
    return None


mouse_.move_to_center()
print('5 secs to start\n')
time.sleep(5)

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

start_time = time.time()
last_x, last_y = mouse_.get_pos()

print(f'started recording: {last_x, last_y}\n')
mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()

with open('mouse_move.json', 'w') as f:
    json.dump(mouse_move, f)

with open('key_down.json', 'w') as f:
    json.dump(key_down, f)

with open('key_up.json', 'w') as f:
    json.dump(key_up, f)

print(f'time recording: {abs(start_time - time.time())}\n')
