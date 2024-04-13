import asyncio
import ctypes
import time
from ctypes import wintypes
from typing import Tuple


class MouseInput(ctypes.Structure):
    """Represents mouse input."""
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)))


class Input(ctypes.Structure):
    """Represents input."""
    _fields_ = (("type", wintypes.DWORD),
                ("mi", MouseInput))


class Point(ctypes.Structure):
    """Represents a point."""
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Mouse:
    """Represents a mouse."""

    def __init__(self, dpi: int, mouse_input_c: type = MouseInput, input_c: type = Input):
        """
        Initializes the Mouse object.

        Args:
            dpi (int): Dots per inch of the screen.
            mouse_input_c (type): Mouse input type.
            input_c (type): Input type.
        """
        speed = ctypes.c_int()
        ctypes.windll.user32.SystemParametersInfoA(112, 0, ctypes.byref(speed), 0)
        self.win_speed = speed.value
        self.mouse_input, self.input = mouse_input_c, input_c
        self.dpi = dpi
        self.input_mouse = 0
        self.mouse_relative, self.mouse_abs = 0x0001, 0x8000
        self.x_size = ctypes.windll.user32.GetSystemMetrics(0)
        self.y_size = ctypes.windll.user32.GetSystemMetrics(1)
        self.now_x, self.now_y = 0, 0
        self.left_down, self.left_up = 0x0002, 0x0004
        self.right_down, self.right_up = 0x0008, 0x0010
        self.x_offset, self.y_offset = 0, 0
        self.user32 = ctypes.windll.user32

    def apply_mult(self, x: int, y: int, mult_x: float, mult_y: float) -> Tuple[int, int]:
        """
        Applies the multiplier to the given coordinates.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            mult_x (float): Multiplier for the X-coordinate.
            mult_y (float): Multiplier for the Y-coordinate.

        Returns:
            Tuple[int, int]: Adjusted X and Y coordinates.
        """
        x_move, y_move = int(mult_x * x), int(mult_y * y)
        self.x_offset += mult_x * x - x_move
        self.y_offset += mult_y * y - y_move

        if abs(int(self.x_offset)) > 0:
            x_move += int(self.x_offset)
            self.x_offset -= int(self.x_offset)

        if abs(int(self.y_offset)) > 0:
            y_move += int(self.y_offset)
            self.y_offset -= int(self.y_offset)
        return x_move, y_move

    def get_pos(self) -> Tuple[int, int]:
        """
        Gets the current mouse position.

        Returns:
            Tuple[int, int]: Current X and Y coordinates of the mouse.
        """
        pt = Point()
        self.user32.GetCursorPos(ctypes.byref(pt))
        self.now_x, self.now_y = pt.x, pt.y
        return self.now_x, self.now_y

    def move_relative(self, x: int, y: int, mult_x: float = 1., mult_y: float = 1.):
        """
        Moves the mouse relatively.

        Args:
            x (int): X-coordinate relative movement.
            y (int): Y-coordinate relative movement.
            mult_x (float, optional): Multiplier for the X-coordinate. Defaults to 1.
            mult_y (float, optional): Multiplier for the Y-coordinate. Defaults to 1.
        """
        x_move, y_move = self.apply_mult(x, y, mult_x, mult_y)
        command = self.mouse_input(x_move, y_move, 0, self.mouse_relative, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def move_absolute(self, x: int, y: int):
        """
        Moves the mouse to absolute coordinates.

        Args:
            x (int): Absolute X-coordinate.
            y (int): Absolute Y-coordinate.
        """
        x = 1 + int(x * 65536. / self.x_size)
        y = 1 + int(y * 65536. / self.y_size)
        command = self.mouse_input(x, y, 0, self.mouse_relative + self.mouse_abs, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def move_to_center(self):
        """Moves the mouse to the center of the screen."""
        self.move_absolute(self.x_size // 2, self.y_size // 2)

    def click_left(self):
        """Simulates a mouse click."""
        command = self.mouse_input(0, 0, 0, self.left_down | self.left_up, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def click_right(self):
        """Simulates a mouse right click."""
        command = self.mouse_input(0, 0, 0, self.right_down | self.right_up, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def down_left(self):
        """Simulates left mouse button down."""
        command = self.mouse_input(0, 0, 0, self.left_down, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def up_left(self):
        """Simulates left mouse button up."""
        command = self.mouse_input(0, 0, 0, self.left_up, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def down_right(self):
        """Simulates right mouse button down."""
        command = self.mouse_input(0, 0, 0, self.right_down, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))

    def up_right(self):
        """Simulates right mouse button up."""
        command = self.mouse_input(0, 0, 0, self.right_up, 0, None)
        settings = self.input(self.input_mouse, command)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(settings), ctypes.sizeof(settings))


class MouseListener:
    def __init__(self, mouse_obj: Mouse):
        self.mouse_obj = mouse_obj
        self.stop_listening = False
        self.time_start = 0
        self.mouse_lb = 0x01
        self.mouse_rb = 0x02
        self.mouse_buttons = {'left': False, 'right': False}
        self.presses = []
        self.releases = []
        self.moves = []

    async def click_listener(self):
        while not self.stop_listening:
            if self.mouse_obj.user32.GetAsyncKeyState(self.mouse_lb) != 0:  # pressed upped left key
                if not self.mouse_buttons['left']:
                    self.presses.append(['left', time.time() - self.time_start])
                    self.mouse_buttons['left'] = True
            elif not self.mouse_obj.user32.GetAsyncKeyState(self.mouse_lb):  # unpressed downed left key
                if self.mouse_buttons['left']:
                    self.releases.append(['left', time.time() - self.time_start])
                    self.mouse_buttons['left'] = False

            if self.mouse_obj.user32.GetAsyncKeyState(self.mouse_rb) != 0:  # pressed upped right key
                if not self.mouse_buttons['right']:
                    self.presses.append(['right', time.time() - self.time_start])
                    self.mouse_buttons['right'] = True
            elif not self.mouse_obj.user32.GetAsyncKeyState(self.mouse_rb):  # unpressed downed right key
                if self.mouse_buttons['right']:
                    self.releases.append(['right', time.time() - self.time_start])
                    self.mouse_buttons['right'] = False

            await asyncio.sleep(0.1)

            print(self.presses, self.releases, sep='\n')
            print()

    async def start_tasks(self):
        clicks = asyncio.create_task(self.click_listener())
        await clicks

    def start_listening(self):
        self.time_start = time.time()
        asyncio.run(self.start_tasks())


# mouse = Mouse(800)
# listener = MouseListener(mouse)
#
# listener.start_listening()
