import stock_utils
import pandas as pd
import plotly.graph_objects as go
import numpy as np

TICKER_SYMBOL = 'TPST'

# Create dataframe
agg_data_df = pd.DataFrame(columns=['Timestamp', 'Sentiment', 'Delta', 'Bull', 'Bear'])

# Loop over TBD number of days
day_list = stock_utils.get_last_x_weekdays(15)
day_list.pop(0)

for day in day_list:
    morning_time_start = day.replace(hour=13, minute=30, second=0, microsecond=0)
    morning_time_end = day.replace(hour=14, minute=0, second=0, microsecond=0)

    df = stock_utils.get_stock_bars(TICKER_SYMBOL, morning_time_start, morning_time_end)
    sentiment, delta_price, bull_count, bear_count = stock_utils.summarize_market_open(df)
    day_name = day.strftime('%A')

    print(
        f"{day_name}({day}) was a {sentiment} with delta of {delta_price:.2f} and {bull_count} :: {bear_count} bullish to bearish candle ratio")

    agg_data_df = agg_data_df.append(
        {'Timestamp': day, 'Sentiment': sentiment, 'Delta': delta_price, 'Bull': bull_count, 'Bear': bear_count},
        ignore_index=True)

print(agg_data_df)
agg_data_df["Color"] = np.where(agg_data_df["Delta"] < 0, 'red', 'green')

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

# fig3 = go.Figure(data = fig.data + fig2.data)
# fig3.show()
# day_list = stock_utils.get_last_x_weekdays(1)
# pm_bar = stock_utils.get_premarket_summary('CZOO', day_list[0])