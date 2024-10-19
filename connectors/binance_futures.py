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
            self._base_url = 'https://testnet.binancefuture.com'
            self._wss_url  = 'wss://stream.binancefuture.com/ws'
        else:
            self._base_url = 'https://fapi.binance.com'
            self._wss_url  = 'wss://fstream.binance.com/ws'

        self._public_key = public_key

        self._secret_key = secret_key

        self._headers = {'X-MBX-APIKEY': self._public_key}

        self.prices = dict()

        self.logs = [] # items to loop and display on UI

        self.contracts = self.get_contracts()
        
        self.balances = self.get_balances()

        self._ws_id = 1

        self.ws = None

        t = threading.Thread(target=self._start_ws)

        #t.start() # prendo y apago el websocket para tener info en tiempo real.
    
        logger.info("Binance Futures Client succesfully started")

    def _add_log(self, msg:str):
        logger.info("%s",msg)
        self.logs.append({"log":msg, "displayed": False})
    
    def _generate_signature(self, data:typing.Dict) -> str:
        return hmac.new(key=self._secret_key.encode() ,msg=urlencode(data).encode(), digestmod= hashlib.sha256).hexdigest()

    
    def _make_request(self, method:str, endpoint:str, data:typing.Dict):
        if method == 'GET':
            try:
                res = requests.get(self._base_url + endpoint, params=data, headers= self._headers)
            except Exception as e:
                logger.error(f'Connection error while making {method} request to {endpoint}: \n{e}')
                return None
        elif method == 'POST':
            try:
                res = requests.post(self._base_url + endpoint, params=data, headers= self._headers)
            except Exception as e:
                logger.error(f'Connection error while making {method} request to {endpoint}: \n{e}')            
                return None
        elif method == 'DELETE':
            try:
                res = requests.delete(self._base_url + endpoint, params=data, headers= self._headers)
            except Exception as e:
                logger.error(f'Connection error while making {method} request to {endpoint}: \n{e}')
                return None
        else:
            raise ValueError()
        
        if res.status_code == 200:
            return res.json()
        else:
            logger.error(f'Error while making a {method} request to {endpoint}: {res.json()} (error status code {res.status_code})')

        return None

    
    def get_contracts(self) -> typing.Dict[str, Contract]:
        exchange_info = self._make_request('GET','/fapi/v1/exchangeInfo', dict())

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['symbol']] = Contract(contract_data)


#                keys_list = list(contracts.keys())
#                #print(contract_data["symbol"])
#                if (keys_list.count(contract_data["pair"]) == 0):  
#                    contracts[contract_data['pair']] = Contract(contract_data)
                #else:
                #    print(f'Key {contract_data["pair"]} already exists')
                    #El symbol "BTCUSDT_240927" tiene el pair BTCUSDT. Por lo que pisaba
                    #El pair original de BTCUSDT. Despues en el suscribe se usa el symbol y
                    #da cualquier cosa. Lo omito porque no se que es ni lo necesito.
        
        return contracts


    def get_historical_candles(self, contract:Contract, interval:str) -> typing.List[Candle]:
        data = dict()
        data['symbol'] = contract.symbol
        data['interval'] = interval
        data['limit'] = 1000

        raw_candles = self._make_request('GET','/fapi/v1/klines',data)

        candles = []

        if raw_candles is not None:
            for candle in raw_candles:
                candles.append(Candle(candle))

        return candles
    
    def get_bid_ask(self, contract:Contract) -> typing.Dict[str, float]:

        data = dict()
        data['symbol'] = contract.symbol
        order_book_data = self._make_request('GET','/fapi/v1/ticker/bookTicker', data)

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
        data['signature'] = self._generate_signature(data)

        balances = dict()

        account_data = self._make_request('GET',"/fapi/v2/account", data)

        if account_data is not None:
            for a in account_data['assets']:
                balances[a['asset']] = Balance(a)

        return balances
    
    def place_order(self, contract:Contract,  order_type:str, quantity:float, side:str, price:float, tif:str, gtd:int ) -> OrderStatus|None:
        data = dict()
        data['symbol'] = contract.symbol
        data['side'] = side
        data['quantity'] = round(round(quantity / contract.lot_size) * contract.lot_size,8)
        data['type'] = order_type

        if price is not None:
            data['price'] = round(round(price / contract.tick_size) * contract.tick_size,8)

        if order_type == 'LIMIT':
            data['timeinforce'] = tif
            data['goodtilldate'] = int(time.time()*100000) + 6000 + gtd #2592000 segundos son 30 dias
        data['timestamp'] = int(time.time()*1000)
        data['signature'] = self._generate_signature(data)
        print('The price to send is going to be: ',data['price'])
        order_status = self._make_request('POST','/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)
            print (f'Order placed sucessfully, order price: {data["price"]}')
        return order_status
    
    def cancel_order(self, contract:Contract, order_id:int) -> OrderStatus|None:
        data = dict()
        data['orderid'] = order_id
        data ['symbol'] = contract.symbol
        data['timestamp'] = int(time.time()*1000)
        data['signature'] = self._generate_signature(data)

        order_status = self._make_request('DELETE','/fapi/v1/order', data)

        if order_status is not None:
            order_status = OrderStatus(order_status)
        
        return order_status
    
    def get_order_status(self, contract:Contract, order_id:int) -> OrderStatus|None:

        data = dict()
        data['timestamp'] = int(time.time()*1000)
        data['symbol'] = contract.symbol
        data['orderid'] = order_id
        data['signature'] = self._generate_signature(data)
        
        order_status = self._make_request(method="GET", endpoint="/fapi/v1/order", data=data)

        if order_status is not None:
            order_status = OrderStatus(order_status)
        
        return order_status
    
    def _start_ws(self):
        #websocket.enableTrace(True) -- Debugger logs
        self.ws = websocket.WebSocketApp(self._wss_url,
                                    on_open    = self._on_open,
                                    on_close   = self._on_close,
                                    on_error   = self._on_error,
                                    on_message = self._on_message)
        while True:
            try:
                self.ws.run_forever()
            except Exception as e:
                logger.error(f'Binance error in run_forever() method: \n{e}')
                time.sleep(5)

    def _on_open(self, ws):
        logger.info("Binance connection opened")

        self.subscribe_channel(list(self.contracts.values()), 'bookTicker') #Siempre se va a suscribir a este contract, habria que cambiar a que contract con un parametro

    def _on_close(self, ws):
        logger.warning("Binance connection closed")

    def _on_error(self, ws, msg:str):
        logger.error(f"Binance connection error: {msg}")

    def _on_message(self,ws, msg:str):

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

                # if symbol == "BTCUSDT" or symbol == 'ETHUSDT':
                #     self._add_log(symbol 
                #                 + " " 
                #                 + str(self.prices[symbol]['bid']) 
                #                 + " / " 
                #                 + str(self.prices[symbol]['ask'])
                #                 )
                print(symbol,": ",self.prices[symbol])


    def subscribe_channel(self, contracts: typing.List[Contract], channel: str):
        data = dict()
        data['method'] = "SUBSCRIBE"
        data['params'] = []
        for contract in contracts:
            data['params'].append(contract.symbol.lower() + "@" + channel)
            data["id"] = self._ws_id

        try:
            self.ws.send(json.dumps(data)) # type: ignore
            print("suscription successful")
        except Exception as e:
            logger.error(f'Websocket error while subscribing to {contract.symbol}: \n{e}')            
            return None

        self._ws_id += 1
        
    
