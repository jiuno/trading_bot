import tkinter as tk
import logging
import pprint as pp
from connectors.binance_futures import BinanceFuturesClient

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)



logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#logger.debug('This is a debug message')
#logger.info('This is an info message')
#logger.warning('This is a warning message')
#logger.error('This is an error message')


if __name__ == '__main__':
    
    binance = BinanceFuturesClient(True)
    #pp.pprint(binance.get_contracts())
    #pp.pprint(binance.get_bid_ask(symbol='BTCUSDT'))
    pp.pprint(binance.get_historical_candles('BTCUSDT', "1h"))

    root = tk.Tk()

    root.mainloop()

