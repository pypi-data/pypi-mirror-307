"""Button class for Tkinter applications."""
import tkinter as tk
from tkinter import ttk

from .constants import PAD, Pad
from .widgets import enter_widget, clickable_widget
from .utilities import invert

ORIENTATION: dict[int, str] | dict[str, int] = {
    0: 'horizontal',
    1: 'vertical',
}
ORIENTATION = invert(ORIENTATION)

VERTICAL = ORIENTATION['vertical']
HORIZONTAL = ORIENTATION['horizontal']


class Button():
    def __init__(
            self,
            text: str,
            command: object,
            sticky: str = '',
            dimmable: bool = False,
            **kwargs: dict,
            ) -> None:

        self.text: str = text,
        self.command: object = command
        self.sticky: str = sticky
        self.underline = None
        self.style = ''
        self.widget = ttk.Button(text=text, command=command)

        self.dimmable = dimmable
        if 'disabled' in kwargs:
            if kwargs['disabled']:
                self.disable()
        if 'underline' in kwargs:
            self.underline = kwargs['underline']
        if 'style' in kwargs:
            self.style = kwargs['style']

    def enable(self, enable: bool = True) -> None:
        state = tk.NORMAL
        if not enable:
            state = tk.DISABLED
        self.widget['state'] = state

    def disable(self, disable: bool = True) -> None:
        state = tk.DISABLED
        if not disable:
            state = tk.NORMAL
        self.widget['state'] = state


class ButtonFrame(ttk.Frame):
    def __init__(self, master: tk.Frame, buttons: list[Button],
                 orientation: int, **kwargs: dict) -> None:
        super().__init__(master, **kwargs)
        self.buttons = buttons
        self._enabled = False

        for button in self.buttons:
            button.widget = ttk.Button(
                self,
                text=button.text,
                command=button.command,
                underline=button.underline,
                )
            if button.style:
                button.widget.configure(style=button.style)

        if orientation == VERTICAL:
            self._vertical_buttons()
        else:
            self._horizontal_buttons()

        if 'enabled' in kwargs:
            self._enabled = kwargs['enabled']

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        state = tk.DISABLED
        if value:
            state = tk.NORMAL
        for button in self. buttons:
            button.widget['state'] = state

    def enable(self, enable: bool = True) -> None:
        self._enabled = enable
        enable_buttons(self.buttons, enable)

    def _vertical_buttons(self) -> None:
        self.rowconfigure(len(self.buttons)-1, weight=1)
        for row, button in enumerate(self.buttons):
            pady = PAD
            if row == 0:
                pady = Pad.S
            if row == len(self.buttons) - 1:
                pady = Pad.N
            if not button.sticky:
                button.sticky = tk.N
            button.widget.grid(row=row, column=0, sticky=button.sticky,
                               pady=pady)
            clickable_widget(button.widget)

    def _horizontal_buttons(self) -> None:
        self.columnconfigure(len(self.buttons)-1, weight=1)
        for col, button in enumerate(self.buttons):
            padx = PAD
            if col == 0:
                padx = Pad.W
            if col == len(self.buttons) - 1:
                padx = Pad.E
            if not button.sticky:
                button.sticky = tk.W
            button.widget.grid(row=0, column=col, sticky=button.sticky,
                               padx=padx)
            clickable_widget(button.widget)


def enable_buttons(buttons: list[Button], enable: bool = True):
    state = tk.NORMAL
    if not enable:
        state = tk.DISABLED
    for button in buttons:
        if button.dimmable:
            button.widget['state'] = state
            button.widget.bind('<Enter>', enter_widget)
