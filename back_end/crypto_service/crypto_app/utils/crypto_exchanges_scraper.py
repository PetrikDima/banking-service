import time
from abc import abstractmethod
from pprint import pprint

import aiohttp
import asyncio


class Exchange:
    """The basic class for Exchanges"""
    BASE_URL = ""
    TRADE_URL_TEMPLATE = ""

    def __init__(self, name):
        self.name = name
        self._prices = {}

    def get_symbol(self, crypto):
        """Method for format trading symbol"""
        return f"{crypto}USDT"

    async def fetch_price(self, session, crypto):
        """Method for fetching price"""
        symbol = self.get_symbol(crypto)
        url = self.BASE_URL.format(symbol=symbol)
        try:
            async with session.get(url) as response:
                data = await response.json()
                price = self.parse_price(data)
                self.set_price(crypto, price)
                return price
        except Exception as e:
            print(f"Error fetching {crypto} from {self.name}: {e}")

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
        if "result" in data and "list" in data["result"]:
            return float(data["result"]["list"][0]["lastPrice"])


class Bitget(Exchange):
    BASE_URL = "https://api.bitget.com/api/v2/spot/market/tickers?category=spot&symbol={symbol}"
    TRADE_URL_TEMPLATE = "https://www.bitget.com/en/spot/{symbol}"

    def parse_price(self, data):
        if "data" in data and isinstance(data["data"], list):
            return float(data["data"][0]["lastPr"])


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
        if "data" in data and isinstance(data["data"], list):
            return float(data["data"][0].get("last", 0))


class CryptoPriceFetcher:
    """Class for getting prices for cryptos from exchanges."""

    def __init__(self):
        self.exchanges = [Binance("Binance"), Bybit("Bybit"), Bitget("Bitget"), KuCoin("KuCoin"), OKX("OKX")]
        self.COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"
        self._cryptos = []

    async def get_top_5_cryptos(self):
        """Method for fetching top 5 cryptos."""
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 6, "page": 1}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.COINGECKO_API, params=params) as resp:
                data = await resp.json()
                self._cryptos = [coin["symbol"].upper() for coin in data if coin["symbol"].upper() != "USDT"][:5]
        return self._cryptos

    async def fetch_prices(self, cryptos):
        """Fetching prices for cryptos from top 5 exchanges."""
        async with aiohttp.ClientSession() as session:
            tasks = [
                exchange.fetch_price(session, crypto)
                for exchange in self.exchanges
                for crypto in cryptos
            ]
            await asyncio.gather(*tasks)

        data = {crypto: {} for crypto in cryptos}

        for exchange in self.exchanges:
            for crypto in cryptos:
                data[crypto][exchange.name] = {
                    "price": exchange.get_price(crypto),
                    "trade_link": exchange.get_trade_url(crypto)
                }

        return data

    async def get_top_5_cryptos_with_prices(self):
        """Method for fetching top 5 cryptos with prices."""
        cryptos = await self.get_top_5_cryptos()
        prices = await self.fetch_prices(cryptos)

        result = {}
        for crypto, values in prices.items():
            result[crypto] = {}
            for exchange, details in values.items():
                result[crypto][exchange] = {
                    "price": details["price"],
                    "trade_link": details["trade_link"]
                }

        return result


if __name__ == "__main__":
    time_before_start = time.time()
    loop = asyncio.get_event_loop()
    fetcher = CryptoPriceFetcher()
    b = loop.run_until_complete(fetcher.get_top_5_cryptos_with_prices())
    pprint(b)
    print(time.time() - time_before_start)