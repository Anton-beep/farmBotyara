from modules.window_manager import WindowManager
from modules.keyboard import Keyboard
from modules.mouse import Mouse
import asyncio
import json
import time
import win32api
import win32con

mouse = Mouse(800)
keyboard = Keyboard()
windows = WindowManager()
windows.find_window_wildcard(".*HELLDIVERS.*")
coefficient = 1


def init_start():
    time.sleep(1)
    keyboard.release_all_keys()
    mouse.up_left()
    mouse.up_right()
    time.sleep(1)
    windows.set_foreground()
    keyboard.type_key('Key.cmd')
    time.sleep(1)
    mouse.move_absolute(100, 5)
    time.sleep(1)
    keyboard.type_key('Key.cmd')
    time.sleep(1)
    mouse.click_left()
    time.sleep(1)
    keyboard.alt_tab()
    time.sleep(1)
    mouse.move_to_center()
    time.sleep(1)
    windows.set_foreground()
    time.sleep(1)
    mouse.click_left()
    mouse.click_left()


async def key_down_event():
    with open('key_down.json', 'r') as f:
        events_key_down = json.load(f)

    for event in events_key_down:
        key = event[0]

        if (time.time() - start_time) < event[1]:
            await asyncio.sleep(event[1] - (time.time() - start_time))

        keyboard.press_key(key)


async def key_up_event():
    with open('key_up.json', 'r') as f:
        events_key_up = json.load(f)

    for event in events_key_up:
        key = event[0]

        if (time.time() - start_time) < event[1]:
            await asyncio.sleep(event[1] - (time.time() - start_time))

        keyboard.release_key(key)


async def mouse_move_event():
    with open('mouse_move.json', 'r') as f:
        events_mouse_move = json.load(f)
    for event in events_mouse_move:
        event_type, *args = event
        if args[-1] > (time.time() - start_time):
            await asyncio.sleep(args[-1] - (time.time() - start_time))
        if event_type == 'move':
            x, y = args[0], args[1]
            mouse.move_relative(x, y, coefficient, coefficient)
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


async def playback_events():
    down_e = asyncio.create_task(key_down_event())
    up_e = asyncio.create_task(key_up_event())
    mouse_e = asyncio.create_task(mouse_move_event())
    await down_e
    await up_e
    await mouse_e
    keyboard.release_all_keys()


# init_start()
mouse.move_to_center()
start_time = time.time()

asyncio.run(playback_events())
