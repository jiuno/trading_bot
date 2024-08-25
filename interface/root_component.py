from interface.styling import *
import tkinter as tk

import time

from interface.logging_component import Logging
from connectors.binance_futures import BinanceFuturesClient

from interface.watchlist_component import Watchlist


class Root(tk.Tk):
    def __init__(self, binance:BinanceFuturesClient):
        super().__init__()

        self.binance = binance
        self.title('Trading Bicho')
        self.configure(bg=BG_COLOR)

        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side = tk.LEFT)

        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side = tk.LEFT)

        self._watchlist_frame = Watchlist(self._left_frame, bg = BG_COLOR)
        self._watchlist_frame.pack(side = tk.TOP )

        self._logging_frame = Logging(self._left_frame, bg = BG_COLOR)
        self._logging_frame.pack(side = tk.TOP )

        self._update_ui()


#        time.sleep(5)
#        self._logging_frame.add_log('This is a test message.')
#        time.sleep(2)
#        self._logging_frame.add_log('2 seconds have passed since last log message.')

    def _update_ui(self):
        for log in self.binance.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True
        
        self.after(1500, self._update_ui)
        
