from interface.styling import BG_COLOR
import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Trading Bicho')
        self.configure(bg=BG_COLOR)

        self.left_frame = tk.Frame(self, bg=BG_COLOR)
        self.left_frame.pack(side = tk.LEFT)

        self.right_frame = tk.Frame(self, bg=BG_COLOR)
        self.right_frame.pack(side = tk.LEFT)


        
