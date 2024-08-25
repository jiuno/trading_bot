import tkinter as tk
import typing

from models import *

from interface.styling import *

class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str, Contract], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binance_symbols = list(binance_contracts.keys())

        #print(self.binance_symbols)

        self._commands_frame = tk.Frame(self, bg=BG_COLOR)
        self._commands_frame.pack(side=tk.TOP)

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)

        self._binance_label = tk.Label(self._commands_frame, text='Binance', fg=FG_COLOR, font=BOLD_FONT
                                       ,bg=BG_COLOR)
        self._binance_label.grid(row = 0, column = 0)

        self._binance_entry = tk.Entry(self._commands_frame, fg=FG_COLOR, justify=tk.CENTER, insertbackground=FG_COLOR, 
                                       bg=BG_COLOR_2)
        self._binance_entry.bind('<Return>', self._add_binance_symbol)
        self._binance_entry.grid(row = 1, column = 0)

        self._headers = ['symbol','exchange','bid','ask']

        for i, e in enumerate(self._headers):
            header = tk.Label(self._table_frame, text=e.capitalize(), bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0,column=i)

    def _add_symbol(self, symbol: str, exchange: str):
        return None
    
    def _add_binance_symbol(self,event):
        symbol = event.widget.get()
        if symbol in self.binance_symbols:
            self._add_symbol(symbol, 'Binance')
            event.widget.delete(0,tk.END) #Deletes what is in the entry box.
