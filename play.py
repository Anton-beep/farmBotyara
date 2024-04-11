import ctypes
from ctypes import wintypes
import json
import time
import win32api
import win32con
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

# Constants extracted from C header files.
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000


# C struct redefinitions.
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)))


class INPUT(ctypes.Structure):
    _fields_ = (("type", wintypes.DWORD),
                ("mi", MOUSEINPUT))


def move_to_center():
    ctypes.windll.user32.SetCursorPos(ctypes.windll.user32.GetSystemMetrics(0) // 2,
                                      ctypes.windll.user32.GetSystemMetrics(1) // 2)


def move_mouse(x, y):
    # x = 1 + int(x * 65536. / ctypes.windll.user32.GetSystemMetrics(0))  # normalize by width
    # y = 1 + int(y * 65536. / ctypes.windll.user32.GetSystemMetrics(1))  # normalize by height
    mi = MOUSEINPUT(x, y, 0, MOUSEEVENTF_MOVE, 0, None)
    ii = INPUT(INPUT_MOUSE, mi)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(ii), ctypes.sizeof(ii))


# Example mapping (you'll need to expand this based on your needs)
VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'space': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
}


def playback_events():
    with open('events.json', 'r') as f:
        events = json.load(f)

    keyboard = KeyboardController()
    mouse = MouseController()
    last_time = 0
    for event in events:
        event_type, *args = event
        current_time = args[-1]
        time.sleep(current_time - last_time)
        last_time = current_time

        if event_type == 'move':
            x, y = args[0], args[1]
            move_mouse(x, y)
        elif event_type == 'click':
            x, y, button, pressed = args[0], args[1], args[2], args[3]
            if pressed:
                if 'Button.left' in button:
                    mouse.press(Button.left)
                elif 'Button.right' in button:
                    mouse.press(Button.right)
            else:
                if 'Button.left' in button:
                    mouse.release(Button.left)
                elif 'Button.right' in button:
                    mouse.release(Button.right)
        elif event_type == 'scroll':
            x, y, dx, dy = args[0], args[1], args[2], args[3]
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, dy, 0)
        elif event_type in ['keypress', 'keyrelease']:
            key = args[0]
            if event_type == 'keypress':
                if key == 'Key.alt_l':
                    keyboard.press(Key.alt_l)
                elif key == 'Key.tab':
                    keyboard.press(Key.tab)
                elif key == 'Key.shift':
                    keyboard.press(Key.shift)
                elif key == 'Key.enter':
                    keyboard.press(Key.enter)
                elif key == 'Key.esc':
                    break
                else:
                    keyboard.press(key)
            elif event_type == 'keyrelease':
                if key == 'Key.alt_l':
                    keyboard.release(Key.alt_l)
                elif key == 'Key.tab':
                    keyboard.release(Key.tab)
                elif key == 'Key.shift':
                    keyboard.press(Key.shift)
                elif key == 'Key.enter':
                    keyboard.press(Key.enter)
                elif key == 'Key.esc':
                    break
                else:
                    keyboard.release(key)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.tab)
    keyboard.release(Key.shift)
    keyboard.release(Key.enter)


time.sleep(1)
move_to_center()
time.sleep(1)
playback_events()