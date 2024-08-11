from interface.styling import *
import tkinter as tk

import time

from interface.logging_component import Logging


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Trading Bicho')
        self.configure(bg=BG_COLOR)

        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side = tk.LEFT)

        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side = tk.LEFT)

        self._logging_frame = Logging(self._left_frame, bg = BG_COLOR)
        self._logging_frame.pack(side = tk.TOP )


        time.sleep(5)
        self._logging_frame.add_log('This is a test message.')
        time.sleep(2)
        self._logging_frame.add_log('2 seconds have passed since last log message.')
        
