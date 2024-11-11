# sdk/example_usage.py
from client import TradingClient

# Assume the user has already obtained their API key via the API





# sdk/example_usage.py

import time
import os
from client import TradingClient, TradingClientException

def run_trading_simulation(api_key, symbols, quantities, wait_time):

    try:
        client = TradingClient(api_key)
    except TradingClientException as e:
        print(f"Failed to initialize TradingClient: {e}")
        return

    for symbol in symbols:
        quantity = quantities.get(symbol, 0.20)  # Default to 0.20 if not specified
        print(f"\n--- Trading for {symbol} ---")

        # Place a MARKET BUY order
        try:
            print(f"Placing MARKET BUY order for {symbol} (Quantity: {quantity})...")
            buy_order_response = client.place_order(
                symbol=symbol,
                quantity=quantity,
                action="BUY",
                order_type="MARKET"
            )
            print(f"BUY Order placed for {symbol}: {buy_order_response}")
        except TradingClientException as e:
            print(f"Error placing BUY order for {symbol}: {e}")
            continue  # Skip to the next symbol

        # Wait for the specified time before placing the SELL order
        print(f"Waiting for {wait_time} seconds before placing SELL order for {symbol}...")
        time.sleep(wait_time)

        # Place a MARKET SELL order
        try:
            print(f"Placing MARKET SELL order for {symbol} (Quantity: {quantity})...")
            sell_order_response = client.place_order(
                symbol=symbol,
                quantity=quantity,
                action="SELL",
                order_type="MARKET"
            )
            print(f"SELL Order placed for {symbol}: {sell_order_response}")
            print(f"Current Balance after selling {symbol}: {sell_order_response.get('balance', 'N/A')}")
        except TradingClientException as e:
            print(f"Error placing SELL order for {symbol}: {e}")
            continue  # Skip to the next symbol

    print("\n--- Trading Simulation Completed ---")


api = "3e1c33ca-8bac-424d-97c2-85e9e545b9af"

# if __name__ == "__main__":
#     api_key = api 

#     if not api_key:
#         print("Error: TRADING_API_KEY environment variable not set.")
#         exit(1)

#     symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "BNBUSDT"]

#     quantities = {
#         "BTCUSDT": 0.5,
#         "ETHUSDT": 1,
#         "SOLUSDT": 10,
#         "ADAUSDT": 100,
#         "BNBUSDT": 10
#     }

#     wait_time = 150  

#     run_trading_simulation(api_key, symbols, quantities, wait_time)



api_key = api 
client = TradingClient(api_key)

import pandas as pd 


try:
    statistics = client.get_trader_statistics()
    statistics = pd.DataFrame([statistics])
    print("Trader Statistics:", statistics)
except Exception as e:
    print("Error fetching trader statistics:", e)



"""
# sdk/example_usage.py

from client import TradingClient

# User provides their API key obtained via the API
api_key = "your_api_key_here"

client = TradingClient(api_key)

# Place a MARKET order
try:
    order_response = client.place_order(
        symbol="BTCUSDT",
        quantity=0.001,
        action="BUY",
        order_type="MARKET"
    )
    print("Market Order placed:", order_response)
except Exception as e:
    print("Error placing MARKET order:", e)

# Place a LIMIT order
try:
    limit_price = 50000  # Example limit price
    order_response = client.place_order(
        symbol="BTCUSDT",
        quantity=0.001,
        action="BUY",
        order_type="LIMIT",
        price=limit_price
    )
    print("Limit Order placed:", order_response)
except Exception as e:
    print("Error placing LIMIT order:", e)

# Place a STOP order
try:
    stop_price = 49000  # Example stop price
    order_response = client.place_order(
        symbol="BTCUSDT",
        quantity=0.001,
        action="SELL",
        order_type="STOP",
        price=stop_price
    )
    print("Stop Order placed:", order_response)
except Exception as e:
    print("Error placing STOP order:", e)


"""