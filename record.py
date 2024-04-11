import ctypes

from pynput import mouse, keyboard
import time
import json

events = []

COEF = 1


def move_to_center():
    ctypes.windll.user32.SetCursorPos(ctypes.windll.user32.GetSystemMetrics(0) // 2,
                                      ctypes.windll.user32.GetSystemMetrics(1) // 2)


user32 = ctypes.windll.user32


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_mouse_pos():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


movements = []

BUFFER_X = 0
BUFFER_Y = 0


def on_move(x, y):
    global start_time, last_x, last_y, movements, BUFFER_X, BUFFER_Y
    x, y = get_mouse_pos()
    dx, dy = x - last_x, y - last_y
    if abs(dx) < 20 and abs(dy) < 20:
        clear_move_x = int(dx * COEF)
        clear_move_y = int(dy * COEF)
        BUFFER_X += dx * COEF - clear_move_x
        BUFFER_Y += dy * COEF - clear_move_y
        events.append(('move', clear_move_x, clear_move_y, time.time() - start_time))
        if abs(BUFFER_X) > 1:
            events.append(('move', int(BUFFER_X), 0, time.time() - start_time))
            BUFFER_X -= int(BUFFER_X)
        if abs(BUFFER_Y) > 1:
            events.append(('move', 0, int(BUFFER_Y), time.time() - start_time))
            BUFFER_Y -= int(BUFFER_Y)
    last_x, last_y = x, y
    # time.sleep(0.001)  # sleep a bit to reduce CPU usage


def on_click(x, y, button, pressed):
    events.append(('click', 0, 0, str(button), pressed, time.time() - start_time))


def on_scroll(x, y, dx, dy):
    events.append(('scroll', x, y, dx, dy, time.time() - start_time))


def on_press(key):
    key = str(key).replace("'", "")
    events.append(('keypress', key, time.time() - start_time))


def on_release(key):
    key = str(key).replace("'", "")
    events.append(('keyrelease', key, time.time() - start_time))
    if key == "Key.esc":
        return False  # Stop listener


move_to_center()

start_time = time.time()
last_x, last_y = get_mouse_pos()

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()

with open('events.json', 'w') as f:
    json.dump(events, f)
