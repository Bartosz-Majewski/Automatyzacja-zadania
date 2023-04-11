import json
from pynput import keyboard, mouse
from time import sleep


class Controller:
    """Control mouse and keyboard"""

    wait = 0.5

    def __init__(self) -> None:
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()

    def click_button(self, button):
        """Click keyboard buttom

        Args:
            button (Button): button to click
        """
        self.keyboard.press(button)
        self.keyboard.release(button)
        sleep(Controller.wait)

    def click_at_position(self, coordinate_x, coordinate_y, button=mouse.Button.left):
        """Set cursor on given position and click button

        Args:
            coordinate_x (int): x position of mouse
            coordinate_y (_type_): y position of mouse
            button (mouse.Button): which mouse button should be it click 
        """
        self.set_position(coordinate_x, coordinate_y)
        sleep(Controller.wait)
        self.mouse.click(button, 1)
        sleep(Controller.wait)

    def press_mouse_button(self, button=mouse.Button.left):
        self.mouse.press(button)
        sleep(Controller.wait)

    def release_mouse_button(self, button=mouse.Button.left):
        self.mouse.release(button)
        sleep(Controller.wait)

    def move_pointer(self, dx=0, dy=0):
        self.mouse.move(
            dx=dx,
            dy=dy
        )
        sleep(Controller.wait)

    def set_position(self, coordinate_x, coordinate_y):
        """Set cursor on given position

            Args:
            coordinate_x (int): x position of mouse
            coordinate_y (_type_): y position of mouse
        """
        self.mouse.position = (coordinate_x, coordinate_y)

    def type(self, text):
        """Type on keyboard

        Args:
            text (str): text to type
        """
        self.keyboard.type(text)
        sleep(Controller.wait)

    def hold_and_press(self, button_to_hold, button_to_press):
        with self.keyboard.pressed(button_to_hold):
            self.click_button(button_to_press)


class Process:
    def __init__(self, file_name, controller):
        self.file_name = file_name
        self.steps = []
        self.controller = controller

    def load_steps(self):
        with open(self.file_name) as file:
            self.steps = json.load(file)['steps']

    def _wait(time):
        sleep(time)

    def _draw_line(self, start_coordinate_x, start_coordinate_y, lenght):
        self.controller.set_position(start_coordinate_x, start_coordinate_y)
        self.controller.press_mouse_button()

        for _ in range(int(lenght/10)):
            self.controller.move_pointer(10)
            sleep(0.1)

        self.controller.release_mouse_button()

    def start(self):
        options = {
            'Type': self.controller.type,
            'Click Button': lambda button: self.controller.click_button(getattr(keyboard.Key, button)),
            'Hold and press': lambda button_to_hold, button_to_press:
                self.controller.hold_and_press(
                    getattr(keyboard.Key, button_to_hold), getattr(keyboard.Key, button_to_press)),
            'Click at positions': lambda coordinate_x, coordinate_y, button:
                self.controller.click_at_position(
                    coordinate_x, coordinate_y, getattr(mouse.Button, button)),
            'Set position': self.controller.set_position,
            'Press mouse button': lambda button:
                self.controller.press_mouse_button(
                    getattr(mouse.Button, button)),
            'Release mouse button': lambda button:
                self.controller.release_mouse_button(
                    getattr(mouse.Button, button)),
            'Draw line': self._draw_line,
            'Wait': self._wait
        }
        for step in self.steps:
            for key, value in step.items():
                options[key](**value)


def main():
    controller = Controller()
    process = Process('actions.json', controller)
    process.load_steps()
    process.start()


if __name__ == '__main__':
    main()
