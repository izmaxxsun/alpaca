from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import config

trading_client = TradingClient(config.PAPER_API_KEY, config.PAPER_SECRET_KEY, paper=True)

account = trading_client.get_account()
for property_name, value in account:
    print(f"{property_name}: {value}")

# Setting params for BUY order
market_order_data = MarketOrderRequest(
    symbol="PLTR",
    qty=1,
    side=OrderSide.BUY,
    extended_hours=True,
    time_in_force=TimeInForce.GTC
)

# Submitting the order and then printing the returned object
market_order = trading_client.submit_order(market_order_data)
for property_name, value in market_order:
  print(f"\"{property_name}\": {value}")