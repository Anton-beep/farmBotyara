import ctypes
import time
from vk_code import VK_CODE
from typing import Union


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
        self.release_key(key)

    def alt_tab(self) -> None:
        """
        Simulates pressing Alt+Tab combination to switch between applications.

        Returns:
            None
        """
        self.press_key('alt')
        self.press_key('tab')
        self.release_key('tab')
        self.release_key('alt')

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
