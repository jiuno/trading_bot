class Balance:
    def __init__(self,balance_info):
        self.initial_margin = float(balance_info['initialMargin'])
        self.maintenance_margin = float(balance_info['maintMargin'])
        self.margin_balance = float(balance_info['marginBalance'])
        self.wallet_balance = float(balance_info['walletBalance'])
        self.unrealized_pnl = float(balance_info['unrealizedProfit'])

class Candle:
    def __init__(self,candle_info) -> None:
        self.timestamp = candle_info[0]
        self.open = float(candle_info[1])
        self.high = float(candle_info[2])
        self.low = float(candle_info[3])
        self.close = float(candle_info[4])
        self.volume = float(candle_info[5])

class Contract:
    def __init__(self,contract_info) -> None:
        self.symbol = contract_info['symbol']
        self.base_asset = contract_info['baseAsset']
        self.quote_asset = contract_info['quoteAsset']
        self.price_decimals = contract_info['pricePrecision']
        self.quantity_decimals = contract_info['quantityPrecision']
        #self.tick_size = 1 / pow(10, contract_info['pricePrecision']) #Tick size no sirve el que trae, hay que modificarlo https://www.binance.com/en/support/announcement/updates-on-the-tick-size-for-btc-usd%E2%93%A2-m-perpetual-futures-contracts-81e6795b0bae49828cbd52479094a987
        self.tick_size = 0.1 #Hardcodeo el tick_size para redondear, por ahora no necesito tanta precision para comprar.
        self.lot_size = 1 / pow(10, contract_info['quantityPrecision'])
class OrderStatus:
    def __init__(self,order_info) -> None:
        self.order_id = order_info['orderId']
        self.status = order_info['status']
        self.avg_price = float(order_info['avgPrice'])
        