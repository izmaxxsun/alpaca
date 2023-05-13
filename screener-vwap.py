import stock_utils
from datetime import datetime, timedelta

# Find stocks above VWAP for past X bars
# Get last X bars for stock
# Get previous day close
# If close price above VWAP for all X bars and above previous day close, return True
today = datetime.today() -timedelta(days=1)
yesterday = today - timedelta(days=3)
df = stock_utils.get_previous_day_close('AAPL', yesterday)

