import tkinter as tk

import typing

from interface.styling import *


class StrategyEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._all_contracts = ['BTCUSDT', 'ETHUSDT']
        self._all_timeframes = ['1m','5m','15m','30m','1h','4h']


        self._commands_frame = tk.Frame(self, bg=BG_COLOR)
        self._commands_frame.pack(side=tk.TOP)

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)

        self._add_button = tk.Button(self._commands_frame, text='Add strategy', font=GLOBAL_FONT
                                     ,command=self._add_strategy_row, bg=BG_COLOR_2 ,fg=FG_COLOR)
        self._add_button.pack(side=tk.TOP)

        self.body_widgets = dict()  #Each column of headers is a column and will be stored as a dictionary. 
                                    #Each key of a specific dictionary/column will be a row.
                                    #Each row will belong to a specific symbol.

        self._headers = ['Strategy','Contract','Timeframe','Balance %', 'TP %' ,'SL %'] 

        self._base_params = [
            {"code_name": "strategy_type","widget": tk.OptionMenu, 'data_type': str, 'values':['Technical','Breakout'], 'width': 7},
            {"code_name": "contract","widget": tk.OptionMenu, 'data_type': str, 'values': self._all_contracts, 'width': 7},            
            {"code_name": "timeframe","widget": tk.OptionMenu, 'data_type': str, 'values': self._all_timeframes, 'width': 7},
            {"code_name": "balance_pct","widget": tk.Entry, 'data_type': float, 'width': 7},
            {"code_name": "take_profit","widget": tk.Entry, 'data_type': float, 'width': 7},
            {"code_name": "stop_loss","widget": tk.Entry, 'data_type': float, 'width': 7},
            {"code_name": "parameters","widget": tk.Button, 'data_type': float, 'text':'Paremeters', 'bg':BG_COLOR_2, 'command': self._show_popup},
            {"code_name": "activation","widget": tk.Button, 'data_type': float, 'text':'OFF', 'bg':'darkred', 'command': self._switch_strategy},
            {"code_name": "delete","widget": tk.Button, 'data_type': float, 'text':'X', 'bg':'darkred', 'command': self._delete_row},

        ]

        for i, h in enumerate(self._headers):
            header = tk.Label(self._table_frame, text=h,bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0,column=i)
        
        for h in self._base_params:
            self.body_widgets[h['code_name']] = dict()
            if h['code_name'] in ['strategy_type','contract','timeframe']: #alternative: if h['widget'] == tk.OptionMenu
                self.body_widgets[h['code_name'] + '_var'] = dict()

        self._body_index = 1 #First row are for headers.

    def _add_strategy_row(self):
        b_index = self._body_index

        for col, base_param in enumerate(self._base_params):
            code_name = base_param['code_name']
            if base_param['widget'] == tk.OptionMenu:
                self.body_widgets[code_name][b_index] = tk.StringVar
                self.body_widgets[code_name][b_index] = tk.OptionMenu(  self._table_frame,
                                                                        self.body_widgets[code_name][b_index],
                                                                        *base_param['values'])
                self.body_widgets[code_name][b_index].config(width = base_param['width'])

            elif base_param['widget'] == tk.Entry:
                self.body_widgets[code_name][b_index] = tk.Entry(self._table_frame,  justify=tk.CENTER)

            elif base_param['widget'] == tk.Button:
                self.body_widgets[code_name][b_index] = tk.Button(self._table_frame,  text=base_param['text'],
                                                                    bg=base_param['bg'],fg=FG_COLOR,
                                                                    command=lambda: base_param['command'](b_index))
            else:
                continue

            self.body_widgets[code_name][b_index].grid(row=b_index, column=col)
            
        self._body_index += 1
    
    def _delete_row(self, b_index: int):
        return

    def _show_popup(self, b_index: int):
        return

    def _switch_strategy(self, b_index: int):
        return

    