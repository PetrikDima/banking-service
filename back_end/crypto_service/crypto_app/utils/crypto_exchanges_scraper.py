import time
from abc import abstractmethod
from datetime import datetime
from pprint import pprint

import requests


class Exchange:
    BASE_URL = ""
    TRADE_URL_TEMPLATE = ""

    def __init__(self, name):
        self.name = name
        self._prices = {}

    def get_symbol(self, crypto):
        return f"{crypto}USDT"

    def fetch_price(self, crypto):
        symbol = self.get_symbol(crypto)
        url = self.BASE_URL.format(symbol=symbol)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = self.parse_price(data)
            self.set_price(crypto, price)
            return price
        except Exception as e:
            print(f"Error fetching {crypto} from {self.name}: {e}")
            return None

    @abstractmethod
    def parse_price(self, data):
        pass

    def get_trade_url(self, crypto):
        return self.TRADE_URL_TEMPLATE.format(symbol=self.get_symbol(crypto))

    def get_price(self, crypto):
        return self._prices.get(crypto, None)

    def set_price(self, crypto, price):
        self._prices[crypto] = price


class Binance(Exchange):
    BASE_URL = "https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    TRADE_URL_TEMPLATE = "https://www.binance.com/en/trade/{symbol}"

    def parse_price(self, data):
        return float(data.get("price", 0))


class Bybit(Exchange):
    BASE_URL = "https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
    TRADE_URL_TEMPLATE = "https://www.bybit.com/en/trade/spot/{symbol}"

    def parse_price(self, data):
        return float(data.get("result", {}).get("list", [{}])[0].get("lastPrice", 0))


class Bitget(Exchange):
    BASE_URL = "https://api.bitget.com/api/v2/spot/market/tickers?category=spot&symbol={symbol}"
    TRADE_URL_TEMPLATE = "https://www.bitget.com/en/spot/{symbol}"

    def parse_price(self, data):
        return float(data.get("data", [{}])[0].get("lastPr", 0))


class KuCoin(Exchange):
    BASE_URL = "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
    TRADE_URL_TEMPLATE = "https://www.kucoin.com/trade/{symbol}"

    def get_symbol(self, crypto):
        return f"{crypto}-USDT"

    def parse_price(self, data):
        return float(data["data"].get("price", 0))


class OKX(Exchange):
    BASE_URL = "https://www.okx.com/api/v5/market/ticker?instId={symbol}"
    TRADE_URL_TEMPLATE = "https://www.okx.com/trade-spot/{symbol}"

    def get_symbol(self, crypto):
        return f"{crypto}-USDT"

    def parse_price(self, data):
        return float(data.get("data", [{}])[0].get("last", 0))


class CryptoPriceFetcher:
    def __init__(self):
        self.exchanges = [Binance("Binance"), Bybit("Bybit"), Bitget("Bitget"), KuCoin("KuCoin"), OKX("OKX")]
        self.COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"
        self._cryptos = []

    def __get_top_5_cryptos(self):
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 6, "page": 1}
        try:
            response = requests.get(self.COINGECKO_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            self._cryptos = [coin["symbol"].upper() for coin in data if coin["symbol"].upper() != "USDT"][:5]
            return self._cryptos
        except Exception as e:
            print(f"Error fetching top cryptos: {e}")
            return []

    def fetch_prices(self, cryptos):
        for exchange in self.exchanges:
            for crypto in cryptos:
                exchange.fetch_price(crypto)

        data = {crypto: {} for crypto in cryptos}
        for exchange in self.exchanges:
            for crypto in cryptos:
                data[crypto][exchange.name] = {
                    "price": exchange.get_price(crypto),
                    "trade_link": exchange.get_trade_url(crypto)
                }

        return data

    def get_top_5_cryptos_with_prices(self):
        cryptos = self.__get_top_5_cryptos()
        return self.fetch_prices(cryptos)

    def fetch_monthly_prices(self) -> dict:
        coingecko_ids = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana",
            "BNB": "binancecoin",
            "XRP": "ripple"
        }

        result = {}
        for symbol, cg_id in coingecko_ids.items():
            url = f"https://api.coingecko.com/api/v3/coins/{cg_id}/market_chart"
            params = {"vs_currency": "usd", "days": 30, "interval": "daily"}
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                daily_prices = []

                for entry in data.get("prices", []):
                    timestamp, price = entry
                    date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                    daily_prices.append({"date": date, "price": round(price, 2)})

                result[symbol] = daily_prices
            except Exception as e:
                print(f"Error fetching monthly price for {symbol}: {e}")

        return result


if __name__ == "__main__":
    time_before_start = time.time()
    fetcher = CryptoPriceFetcher()

    print("Top 5 cryptos with prices:")
    b = fetcher.get_top_5_cryptos_with_prices()
    pprint(b)

    print("\nMonthly price history:")
    monthly_data = fetcher.fetch_monthly_prices()
    pprint(monthly_data)

    print(f"\nExecution time: {time.time() - time_before_start:.2f} seconds")
