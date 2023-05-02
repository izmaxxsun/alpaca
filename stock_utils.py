import pandas as pd
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import StockLatestBarRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

API_KEY = 'AK1CA7CG5MJXIK4WTBBP'
SECRET_KEY = 'AaVB3kFzvnujNwHepEfZRcoOQkHakXGBRPzAtCBM'
stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)


def summarize_market_open(bars_df):
    """ Assessment of initial wash or perk up on market open

    Uses delta in price for the first 30 minutes and counts of bullish-bearish candles
    TODO - review logic on gauging notable dip/perk

    :param bars_df:
    :return: count of bullish and bearish candles
    """
    bull_count = 0
    bear_count = 0
    sentiment = ''

    open_price = bars_df.head(1)['open'].iat[0]
    close_price = bars_df.tail(1)['close'].iat[0]
    delta_price = close_price - open_price

    for index, row in bars_df.iterrows():
        #print(str(row['timestamp']))
        open = row['open']
        close = row['close']
        result = close - open
        if result <= 0:
            bear_count += 1
        else:
            bull_count += 1

    #print(f"Bull count: {bull_count}")
    #print(f"Bear count: {bear_count}")

    if delta_price > 0:
        # Bullish
        if bull_count > bear_count:
            sentiment = 'perk'
        else:
            sentiment = 'indeterminate'
    else:
        # Bearish
        if bear_count > bull_count:
            sentiment = 'dip'
        else:
            sentiment = 'indeterminate'

    return sentiment, delta_price, bull_count, bear_count


def get_stock_bars(symbol, start_date, end_date):
    """ Retrieves candle information for a given stock

    :param symbol: Ticker for stock
    :param start_date: Start of time period in UTC
    :param end_date: End of time period in UTC
    :return: Data frame containing candles
    """
    request_params = StockBarsRequest(symbol_or_symbols=[symbol],
                                      timeframe=TimeFrame.Minute,
                                      start=start_date,
                                      end=end_date)
    am_bar = stock_client.get_stock_bars(request_params)
    frc = am_bar[symbol]
    df = pd.DataFrame([o.__dict__ for o in frc])
    df = df.iloc[:, 1:]
    return df


def is_weekday(date: datetime):
    """ Determines whether given date is a weekday

    :param date: Date to check
    :return: Boolean indicating whether this is a weekday
    """
    weekday_number = date.weekday()
    if weekday_number < 5:
        weekday_bool = True
    else:
        weekday_bool = False
    return weekday_bool


def get_last_x_weekdays(num_weekdays):
    lookback_period = num_weekdays
    day_list = []
    day = datetime.now()

    while lookback_period > 0:
        if is_weekday(day):
            day_list.append(day)
            lookback_period -= 1
        day = day - timedelta(days=1)

    return day_list


def get_premarket_summary(symbol:str, date:datetime):
    """ Get premarket high, low, and market open values. 4am ET to 9:30am ET

    :param symbol: Stock ticker
    :param date: Date with only day specified
    :return:
    """
    start_time = date.replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = date.replace(hour=13, minute=30, second=0, microsecond=0)
    pm_bars = get_stock_bars(symbol, start_time, end_time)
    print(pm_bars)
    print(pm_bars.close.max())


def get_previous_day_close(symbol:str, date:datetime):
    pass


def calculate_central_pivot_range():
    #https://tradingtuitions.com/all-you-wanted-to-know-about-central-pivot-range-cpr-indicator/
    pass

