from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import StockLatestBarRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pandas as pd


API_KEY = 'AK1CA7CG5MJXIK4WTBBP'
SECRET_KEY = 'AaVB3kFzvnujNwHepEfZRcoOQkHakXGBRPzAtCBM'
SYMBOL = 'AAPL'

stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

today = datetime.today()
start_time = today.replace(hour=8, minute=0, second=0, microsecond=0)
end_time = today.replace(hour=13, minute=30, second=0, microsecond=0)

request_params = StockBarsRequest(symbol_or_symbols=[SYMBOL],
                                      timeframe=TimeFrame.Minute,
                                      start=start_time,
                                      end=end_time)
am_bar = stock_client.get_stock_bars(request_params)
stock_bars = am_bar[SYMBOL]
df = pd.DataFrame([o.__dict__ for o in stock_bars])
df = df.iloc[:, 1:]

print(df)