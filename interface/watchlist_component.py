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

        self.body_widgets = dict()  #Each column of headers is a column and will be stored as a dictionary. 
                                    #Each key of a specific dictionary/column will be a row.
                                    #Each row will belong to a specific symbol.

        self._headers = ['symbol','exchange','bid','ask','remove'] 

        for i, h in enumerate(self._headers):
            header = tk.Label(self._table_frame, text=h.capitalize() if h != 'remove' else "",
                                bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0,column=i)
        
        for h in self._headers:
            self.body_widgets[h] = dict()
            if h in ["bid","ask"]:
                self.body_widgets[h+"_var"] = dict() 

        self._body_index = 1 #First row are for headers.

    def _remove_symbol(self, b_index: int):
        for h in self._headers:
            self.body_widgets[h][b_index].grid_forget()
        del self.body_widgets[h][b_index]


        return None


    def _add_symbol(self, symbol: str, exchange: str):
        b_index = self._body_index #Rename to a shorter version

        self.body_widgets['symbol'][b_index] = tk.Label(self._table_frame,
                                                        text=symbol,
                                                        bg = BG_COLOR,
                                                        fg = FG_COLOR_2,
                                                        font = GLOBAL_FONT)
        self.body_widgets['symbol'][b_index].grid(row=b_index,column = 0)

        self.body_widgets['exchange'][b_index] = tk.Label(self._table_frame,
                                                        text=exchange,
                                                        bg = BG_COLOR,
                                                        fg = FG_COLOR_2,
                                                        font = GLOBAL_FONT)
        

        
        self.body_widgets['exchange'][b_index].grid(row=b_index,column = 1)

        self.body_widgets['bid_var'][b_index] = tk.StringVar()

        self.body_widgets['bid'][b_index] = tk.Label(self._table_frame,
                                                        textvariable=self.body_widgets['bid_var'][b_index],
                                                        bg = BG_COLOR,
                                                        fg = FG_COLOR_2,
                                                        font = GLOBAL_FONT)
        
        self.body_widgets['bid'][b_index].grid(row=b_index,column = 2)



        self.body_widgets['ask_var'][b_index] = tk.StringVar()

        self.body_widgets['ask'][b_index] = tk.Label(self._table_frame,
                                                        textvariable=self.body_widgets['ask_var'][b_index],
                                                        bg = BG_COLOR,
                                                        fg = FG_COLOR_2,
                                                        font = GLOBAL_FONT)
        
        self.body_widgets['ask'][b_index].grid(row=b_index,column = 3)

        self.body_widgets['remove'][b_index] = tk.Button(self._table_frame,
                                                        text = "X",
                                                        bg = "darkred",
                                                        fg = FG_COLOR,
                                                        font = GLOBAL_FONT,
                                                        command=lambda: self._remove_symbol(b_index)) #lambda only for callback functions that need args. Else it will execute when add symbol is called.
        
        self.body_widgets['remove'][b_index].grid(row=b_index,column = 4)

        self._body_index += 1


        
        
        return None
    
    def _add_binance_symbol(self,event):
        symbol = event.widget.get()
        if symbol in self.binance_symbols:
            self._add_symbol(symbol, 'Binance')
            event.widget.delete(0,tk.END) #Deletes what is in the entry box.
