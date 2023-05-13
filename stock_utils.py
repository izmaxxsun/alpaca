from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import StockLatestBarRequest, StockBarsRequest, StockSnapshotRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import numpy as np

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

def get_stock_snapshot(symbol):
    """ Retrieves previous daily candle

    :param symbol:
    :return:
    """

    request_params = StockSnapshotRequest(symbol_or_symbols=[symbol])
    snapshot = stock_client.get_stock_snapshot(request_params)
    return snapshot



def get_stock_bars(symbol, start_date, end_date, time_frame=TimeFrame.Minute):
    """ Retrieves candle information for a given stock

    :param symbol: Ticker for stock
    :param start_date: Start of time period in UTC
    :param end_date: End of time period in UTC
    :return: Data frame containing candles
    """
    request_params = StockBarsRequest(symbol_or_symbols=[symbol],
                                      timeframe=time_frame,
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


def get_previous_day_close(symbol: str, date: datetime):
    # TODO: Complete
    """ Gets previous day close

    :param symbol: ticker symbol
    :param date: The current day
    :return:
    """
    #get_stock_bars(symbol, )
    df = get_stock_bars(symbol, date, date + timedelta(days=1), TimeFrame.Day)
    print(df)

def calculate_central_pivot_range(symbol: str, date: datetime):
    # TODO: Complete
    #https://tradingtuitions.com/all-you-wanted-to-know-about-central-pivot-range-cpr-indicator/
    # TC = (Pivot – BC) + Pivot
    # Pivot = (High + Low + Close) / 3
    # BC = (High + Low) / 2
    pass

def get_market_open_probability(ticker, lookback_days):
    # Create dataframe
    agg_data_df = pd.DataFrame(columns=['Timestamp', 'Sentiment', 'Delta', 'Bull', 'Bear'])

    # Loop over TBD number of days
    day_list = get_last_x_weekdays(15)
    day_list.pop(0)

    for day in day_list:
        morning_time_start = day.replace(hour=13, minute=30, second=0, microsecond=0)
        morning_time_end = day.replace(hour=14, minute=0, second=0, microsecond=0)

        df = get_stock_bars(ticker, morning_time_start, morning_time_end)
        sentiment, delta_price, bull_count, bear_count = summarize_market_open(df)
        day_name = day.strftime('%A')

        print(
            f"{day_name}({day}) was a {sentiment} with delta of {delta_price:.2f} and {bull_count} :: {bear_count} bullish to bearish candle ratio")

        agg_data_df = agg_data_df.append(
            {'Timestamp': day, 'Sentiment': sentiment, 'Delta': delta_price, 'Bull': bull_count, 'Bear': bear_count},
            ignore_index=True)

    print(agg_data_df)
    agg_data_df["Color"] = np.where(agg_data_df["Delta"] < 0, 'red', 'green')

    red_count = len(agg_data_df[agg_data_df['Color'] == 'red'])
    green_count = len(agg_data_df[agg_data_df['Color'] == 'green'])
    probability_opening_perk = green_count / (red_count + green_count)
    delta_avg = agg_data_df.loc[agg_data_df['Delta'] > 0, 'Delta'].mean()

    print(f"Probability of market open perk: {probability_opening_perk:.2%} with avg delta of ${delta_avg:.2f}")


    fig = go.Figure(data=[go.Bar(
        x=agg_data_df.Timestamp, y=agg_data_df.Delta,
        text=agg_data_df.Sentiment,
        marker_color=agg_data_df.Color,
        textposition='auto',
    )])

    fig.show()

    # Plot
    fig2 = go.Figure(data=[
        go.Bar(name='Bull', x=agg_data_df.Timestamp, y=agg_data_df.Bull, marker = dict(color='Green')),
        go.Bar(name='Bear', x=agg_data_df.Timestamp, y=agg_data_df.Bear, marker = dict(color='Red'))
    ])
    # Change the bar mode
    fig2.update_layout(barmode='stack')
    fig2.show()