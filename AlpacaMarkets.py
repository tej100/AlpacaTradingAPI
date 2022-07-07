import requests
import json
import pandas as pd


class TradingAPI:
    def __init__(self, Alpaca_KeyID, Alpaca_SecretKey):
        """
        After setting up your Alpaca Brokerage Account, get your
        api key and secret key to connect to your account. Then,
        start trading as you wish
        """
        self.BASE_URL = "https://paper-api.alpaca.markets"
        self.ACCOUNT_URL = f"{self.BASE_URL}/v2/account"
        self.ORDERS_URL = f"{self.BASE_URL}/v2/orders"
        self.POSITIONS_URL = f"{self.BASE_URL}/v2/positions"
        self.PORTFOLIO_URL = f"{self.ACCOUNT_URL}/portfolio/history"
        self.HEADERS = {'APCA-API-KEY-ID': Alpaca_KeyID, 'APCA-API-SECRET-KEY': Alpaca_SecretKey}

    def GetAccount(self):
        r = requests.get(self.ACCOUNT_URL, headers=self.HEADERS)
        return json.loads(r.content)

    def CreateOrder(self, symbol, qty, side, *, type='market', time_in_force='gtc', limit_price=0, trail_percent=0):
        """
        Create an order to trade on Alpaca Paper Trading Account

        :param str symbol: ticker symbol of stock to order
        :param int qty: number of shares to order
        :param str side: 'buy' or 'sell'
        :param str type: 'market', 'limit', 'trailing_stop'
        :param str time_in_force: 'day', 'gtc'
        :param float limit_price: price that you want the order to execute at
        :param float trail_percent: percentage
        """
        limit_price = str(limit_price)
        trail_percent = str(trail_percent)

        if type == 'limit':
            data = {
                "symbol": symbol,
                "qty": qty,
                "side": side,
                "type": 'limit',
                "time_in_force": time_in_force,
                "limit_price": limit_price,
            }
        elif type == 'trailing_stop':
            data = {
                "symbol": symbol,
                "qty": qty,
                "side": side,
                "type": 'trailing_stop',
                "time_in_force": time_in_force,
                "trail_percent": trail_percent
            }
        else:  # If type is default, market
            data = {
                "symbol": symbol,
                "qty": qty,
                "side": side,
                "type": 'market',
                "time_in_force": time_in_force,
            }
        r = requests.post(self.ORDERS_URL, json=data, headers=self.HEADERS)
        return json.loads(r.content)

    def GetOrders(self, status="open", symbols=""):
        data = {
            "status": status,
            "symbols": symbols
        }
        r = requests.get(self.ORDERS_URL, params=data, headers=self.HEADERS)
        return json.loads(r.content)

    def CurrentPositions(self, symbol='') -> bool:
        """
        Outputs True or False based on if there is a
        current open position of the input symbol
        :param str symbol: default is all positions, otherwise indicate ticker
        """
        positions_url = f"{self.POSITIONS_URL}/{symbol}"
        r = requests.get(positions_url, headers=self.HEADERS)
        positions_dict = json.loads(r.content)
        if 'symbol' in positions_dict:
            return True
        else:
            return False

    def ClosePosition(self, symbol):
        """
        Closes an existing position or all positions
        :param str symbol: indicate '' to delete all positions, otherwise indicate ticker symbol
        """
        positions_url = f"{self.POSITIONS_URL}/{symbol}"
        r = requests.delete(positions_url, headers=self.HEADERS)
        return json.loads(r.content)

    def PortfolioHistory(self, *, period='1M', timeframe='1D', to_csv=False) -> pd.DataFrame:
        """
        Return portolio history data in pandas dataframe (earliest start is start of portfolio)
        """
        data = {
            "period": period,
            "timeframe": timeframe
        }
        r = requests.get(self.PORTFOLIO_URL, params=data, headers=self.HEADERS)
        port_hist = pd.DataFrame(json.loads(r.content))
        port_hist.set_index('timestamp', inplace=True)
        port_hist = port_hist[port_hist['equity'] != 0]

        if to_csv:
            port_hist.to_csv(path_or_buf="Alpaca_Portfolio_History.csv", mode='w', header=True)

        return port_hist
