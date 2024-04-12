import ctypes
import time
from typing import Union

VK_CODE = {
    'backspace': 0x08,
    'Key.tab': 0x09,
    'Key.enter': 0x0D,
    'Key.shift': 0x10,
    'Key.ctrl_l': 0x11,
    'Key.alt_l': 0x12,
    'pause': 0x13,
    'Key.caps_lock': 0x14,
    'Key.esc': 0x1B,
    'Key.cmd': 0x5B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'insert': 0x2D,
    'delete': 0x2E,
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
    "'": 0xDE
}


class Keyboard:
    """
    A class for simulating keyboard input using ctypes.

    Attributes:
        user32 (ctypes.windll.user32): A reference to the user32.dll library.
    """

    def __init__(self) -> None:
        """
        Initializes the Keyboard object.
        """
        self.user32 = ctypes.windll.user32

    def press_key(self, key: str) -> None:
        """
        Simulates pressing the specified key.

        Args:
            key (str): The key to press.

        Returns:
            None
        """
        self.user32.keybd_event(VK_CODE[key], 0, 0, 0)

    def release_key(self, key: str) -> None:
        """
        Simulates releasing the specified key.

        Args:
            key (str): The key to release.

        Returns:
            None
        """
        self.user32.keybd_event(VK_CODE[key], 0, ctypes.c_uint(0x0002), 0)

    def type_key(self, key: str) -> None:
        """
        Simulates typing the specified key (pressing and releasing).

        Args:
            key (str): The key to type.

        Returns:
            None
        """
        self.press_key(key)
        time.sleep(0.01)
        self.release_key(key)

    def alt_tab(self) -> None:
        """
        Simulates pressing Alt+Tab combination to switch between applications.

        Returns:
            None
        """
        self.press_key('Key.alt_l')
        self.press_key('Key.tab')
        self.release_key('Key.tab')
        self.release_key('Key.alt_l')

    def press_key_for_time(self, key: str, duration: Union[int, float]) -> None:
        """
        Presses the specified key for a given duration before releasing it.

        Args:
            key (str): The key to press.
            duration (Union[int, float]): The duration for which to press the key, in seconds.

        Returns:
            None
        """
        self.press_key(key)
        time.sleep(duration)
        self.release_key(key)

    def release_all_keys(self):
        """
        Releases all keys that are currently pressed.
        """
        for key in VK_CODE:
            self.release_key(key)
