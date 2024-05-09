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
    
    binance = BinanceFuturesClient(public_key="81ce10e167a9d66cc90196cfd855e9663520c5c01fcb0ff9d1631e7339acca14",
                                   secret_key="143bdd888d0c98e13511ffe71dc229ae393c9997686136b3c16b632494a589b1",
                                   testnet=True)
    #pp.pprint(binance.get_contracts())
    #pp.pprint(binance.get_bid_ask(symbol='BTCUSDT'))
    pp.pprint(binance.get_balances())

    root = tk.Tk()

    root.mainloop()
