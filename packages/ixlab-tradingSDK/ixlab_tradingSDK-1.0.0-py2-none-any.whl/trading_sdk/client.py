# sdk/client.py

import aiohttp
import asyncio

class TradingClientException(Exception):
    pass

class TradingClient:
    def __init__(self, api_key, base_url="http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'api-key': self.api_key}

    async def _handle_response(self, response):
        if response.status == 200:
            return await response.json()
        else:
            error_message = await response.text()
            raise TradingClientException(f"Error {response.status}: {error_message}")

    async def place_order(self, symbol, quantity, action, order_type, price=None):
        url = f"{self.base_url}/order"
        data = {
            'symbol': symbol,
            'quantity': quantity,
            'action': action.upper(),
            'order_type': order_type.upper()
        }
        if price is not None:
            data['price'] = price

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=data) as response:
                return await self._handle_response(response)

    async def get_order_history(self):
        url = f"{self.base_url}/orders"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                return await self._handle_response(response)

    async def get_open_positions(self):
        url = f"{self.base_url}/positions"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                return await self._handle_response(response)

    async def get_trading_journal(self):
        url = f"{self.base_url}/journal"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                return await self._handle_response(response)

    async def get_trader_statistics(self):
        url = f"{self.base_url}/statistics"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                return await self._handle_response(response)
