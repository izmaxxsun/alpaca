import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])])

fig.update_layout(xaxis_rangeslider_visible=False)
# make space for explanation / annotation
fig.update_layout(margin=dict(l=20, r=20, t=20, b=60),paper_bgcolor="white")

# add annotation
fig.add_annotation(dict(font=dict(color='black',size=20),
                                        x=0,
                                        y=-0.12,
                                        showarrow=False,
                                        text="Red green",
                                        textangle=0,
                                        xanchor='left',
                                        xref="paper",
                                        yref="paper"))

fig.show()