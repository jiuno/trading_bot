import tkinter as tk
from datetime import datetime

from interface.styling import *

class Logging(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Instantiates a frame

        self.logging_text = tk.Text(self,
                                     height= 10,
                                     width= 60,
                                     state = tk.DISABLED, #Se bloquea para que nadie pueda escribir, user o sys
                                     bg=BG_COLOR,
                                     fg=FG_COLOR_2,
                                     font= GLOBAL_FONT)
        self.logging_text.pack(side=tk.TOP)

    def add_log(self,message:str):
        self.logging_text.configure(state=tk.NORMAL) #desbloqueamos el txt widget

        self.logging_text.insert('1.0', datetime.now().strftime("%b %d  %H:%M:%S ::") + message + '\n') #1.0 shows message at the top of widget.

        self.logging_text.configure(state=tk.DISABLED)
