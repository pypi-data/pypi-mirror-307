"""Various Tkinter widgets and methods."""
import tkinter as tk
from tkinter import ttk
import contextlib

from .constants import PAD
HAND = 'hand2'
DIM_TEXT = '#555'


class PsiText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that reports on internal widget commands."""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


def get_styles() -> ttk.Style:
    style = ttk.Style()
    style.configure('red.Label', foreground='red')
    style.configure('green.Label', foreground='green')
    style.configure('blue.Label', foreground='blue')
    style.configure('yellow.Label', foreground='yellow')
    style.configure('grey.Label', foreground='grey')

    style.map('data.TEntry',
              fieldbackground=[
                  ('focus', '#eee'),
                  ('disabled', 'lightgrey'),
                  ('invalid', 'pink'),
                  ])

    style.configure('red.TFrame', background='red')
    style.configure('green.TFrame', background='green')
    style.configure('blue.TFrame', background='blue')
    style.configure('yellow.TFrame', background='yellow')
    style.configure('grey.TFrame', background='grey ')
    style.map('Treeview',
              foreground=fixed_map(style, 'foreground'),
              background=fixed_map(style, 'background'))

    return style


def fixed_map(style, option):
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map('Treeview', query_opt=option)
            if elm[:2] != ('!disabled', '!selected')]


def vertical_scroll_bar(
        master: tk.Frame,
        widget: tk.Widget,
        ) -> ttk.Scrollbar:

    v_scroll = ttk.Scrollbar(
        master,
        orient='vertical',
        command=widget.yview
        )
    widget.configure(yscrollcommand=v_scroll.set)
    widget['yscrollcommand'] = v_scroll.set
    return v_scroll


def enter_widget(event: object = None) -> None:
    if tk.DISABLED in event.widget.state():
        return
    event.widget.winfo_toplevel().config(cursor=HAND)


def _leave_widget(event: object = None) -> None:
    event.widget.winfo_toplevel().config(cursor='')


def clickable_widget(widget: object) -> None:
    widget.bind('<Enter>', enter_widget)
    widget.bind('<Leave>', _leave_widget)


def status_bar(master: tk.Frame, textvariable: tk.StringVar,
               colour: str = DIM_TEXT) -> tk.Frame:
    frame = ttk.Frame(master, relief=tk.SUNKEN)
    frame.columnconfigure(1, weight=1)
    label = tk.Label(frame, fg=colour, textvariable=textvariable)
    label.grid(row=0, column=0, sticky=tk.W, padx=PAD, pady=1)
    return frame


@contextlib.contextmanager
def WaitCursor(root):
    root.config(cursor='watch')
    root.update()
    try:
        yield root
    finally:
        root.config(cursor='')


def separator_frame(master: tk.Frame, text: str) -> tk.Frame:
    frame = ttk.Frame(master)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(2, weight=1)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=0, column=0, sticky=tk.EW, padx=PAD, pady=PAD*4)

    label = ttk.Label(frame, text=text)
    label.grid(row=0, column=1, sticky=tk.E)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=0, column=2, sticky=tk.EW, padx=PAD)
    return frame
