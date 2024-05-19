import logging
import time
import requests
import typing
import hmac
import hashlib
from urllib.parse import urlencode
import websocket
import threading
import json
from models import *

logger = logging.getLogger()

class BinanceFuturesClient:
    def __init__(self, public_key:str, secret_key:str, testnet:bool):
        if testnet:
            self.base_url = 'https://testnet.binancefuture.com'
            self.wss_url  = 'wss://stream.binancefuture.com/ws'
        else:
            self.base_url = 'https://fapi.binance.com'
            self.wss_url  = 'wss://fstream.binance.com/ws'

        self.public_key = public_key

        self.secret_key = secret_key

        self.headers = {'X-MBX-APIKEY': self.public_key}

        self.prices = dict()


        self.contracts = self.get_contracts()
        
        self.balances = self.get_balances()

        self.id = 1

        self.ws = None

        t = threading.Thread(target=self.start_ws)

        #t.start() -- prendo y apago el websocket para tener info en tiempo real.
    
        logger.info("Binance Futures Client succesfully started")
    
    def generate_signature(self, data:typing.Dict) -> str:
        return hmac.new(key=self.secret_key.encode() ,msg=urlencode(data).encode(), digestmod= hashlib.sha256).hexdigest()

    
    def make_request(self, method:str, endpoint:str, data:typing.Dict):
        if method == 'GET':
           res = requests.get(self.base_url + endpoint, params=data, headers= self.headers)
        elif method == 'POST':
            res = requests.post(self.base_url + endpoint, params=data, headers= self.headers)
        elif method == 'DELETE':
            res = requests.delete(self.base_url + endpoint, params=data, headers= self.headers)

        else:
            raise ValueError()
        
        if res.status_code == 200:
            return res.json()
        else:
            logger.error(f'Error while making a {method} request to {endpoint}: {res.json()} (error status code {res.status_code})')

        return None

    
    def get_contracts(self) -> typing.Dict[str, Contract]:
        exchange_info = self.make_request('GET','/fapi/v1/exchangeInfo', dict())

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = Contract(contract_data)
        
        return contracts


    def get_historical_candles(self, contract:Contract, interval:str) -> typing.List[Candle]:
        data = dict()
        data['symbol'] = contract.symbol
        data['interval'] = interval
        data['limit'] = 1000

        raw_candles = self.make_request('GET','/fapi/v1/klines',data)

        candles = []

        if raw_candles is not None:
            for candle in raw_candles:
                candles.append(Candle(candle))

        return candles
    
    def get_bid_ask(self, contract:Contract) -> typing.Dict[str, float]:

        data = dict()
        data['symbol'] = contract.symbol
        order_book_data = self.make_request('GET','/fapi/v1/ticker/bookTicker', data)

        if order_book_data is not None:
            if contract.symbol not in self.prices:
                self.prices[contract.symbol] = {'bid' : float(order_book_data['bidPrice']),
                                       'ask' : float(order_book_data['askPrice'])}
            else:
                self.prices[contract.symbol]['bid'] = float(order_book_data['bidPrice'])
                self.prices[contract.symbol]['ask'] = float(order_book_data['askPrice'])
        
        return self.prices[contract.symbol]
    
    def get_balances(self) -> typing.Dict[str, Balance]:
        data = dict()
        data['timestamp'] = int(time.time()*1000)
        data['signature'] = self.generate_signature(data)

        balances = dict()

        account_data = self.make_request('GET',"/fapi/v2/account", data)

        if account_data is not None:
            for a in account_data['assets']:
                balances[a['asset']] = Balance(a)

        return balances
    
    def place_order(self, contract:Contract, side:str, quantity:float, order_type:str, price=None, tif=None) -> OrderStatus:
        data = dict()
        data['symbol'] = contract.symbol
        data['side'] = side
        data['quantity'] = quantity
        data['type'] = order_type

        if price is not None:
            data['price'] = price
        if tif is not None:
            data['timeinforce'] = tif
        data['timestamp'] = int(time.time()*1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request('POST','/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)
            
        return order_status
    
    def cancel_order(self, contract:Contract, order_id:int) -> OrderStatus:
        data = dict()
        data['orderid'] = order_id
        data ['symbol'] = contract.symbol
        data['timestamp'] = int(time.time()*1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request('DELETE','/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)
        
        return order_status
    
    def get_order_status(self, contract:Contract, order_id:int) -> OrderStatus:

        data = dict()
        data['timestamp'] = int(time.time()*1000)
        data['symbol'] = contract.symbol
        data['orderid'] = order_id
        data['signature'] = self.generate_signature(data)
        
        order_status = self.make_request(method="GET", endpoint="/fapi/v1/order", data=data)

        if order_status is not None:
            order_status = OrderStatus(order_status)
        
        return order_status
    
    def start_ws(self):
        self.ws = websocket.WebSocketApp(self.wss_url,
                                    on_open    = self.on_open,
                                    on_close   = self.on_close,
                                    on_error   = self.on_error,
                                    on_message = self.on_message)
        self.ws.run_forever()
    
    def on_open(self, ws):
        logger.info("Binance connection opened")

        self.subscribe_channel(self.contracts['BTCUSDT']) #Siempre se va a suscribir a este contract, habria que cambiar a que contract con un parametro

    def on_close(self, ws):
        logger.warning("Binance connection closed")

    def on_error(self, ws, msg:str):
        logger.error(f"Binance connection error: {msg}")

    def on_message(self,ws, msg:str):
#        print(msg)

        data = json.loads(msg)

        if "e" in data:
            if data["e"] == "bookTicker":

                symbol = data["s"]

                if symbol not in self.prices:
                    self.prices[symbol] = { 'bid' : float(data['b']),
                                            'ask' : float(data['a'])}
                else:
                    self.prices[symbol]['bid'] = float(data['b'])
                    self.prices[symbol]['ask'] = float(data['a'])

                print(self.prices[symbol])


    def subscribe_channel(self, contract:Contract):
        data = dict()
        data['method'] = "SUBSCRIBE"
        data['params'] = []
        data['params'].append(contract.symbol.lower() + "@bookTicker")
        data["id"] = self.id

        self.ws.send(json.dumps(data))
        
        self.id += 1
        
    
