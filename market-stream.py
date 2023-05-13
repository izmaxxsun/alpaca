import json
import websocket
import pandas as pd
import config
from stock import Stock

SYMBOL = 'CVNA'

stock = Stock(SYMBOL)
print(f"Previous close for {stock.symbol} is {stock.prev_close}")

bars_df = pd.DataFrame()

def on_open(ws):
    print("Opened web socket connection")
    auth_data = {
        "action": "auth",
        "key": config.API_KEY,
        "secret": config.SECRET_KEY
    }

    ws.send(json.dumps(auth_data))

    channel_data = {
        "action": "subscribe",
        "bars": [SYMBOL]
    }
    # {"action":"subscribe","bars":["AAPL"]}

    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    parse = json.loads(message)

    for bar in parse:
        if bar.get('S') is None:
            pass
            # print('not a bar')
        else:
            try:
                print(f"Bar: {bar}")
                stock.update_latest_close(bar['c'])
                stock.update_latest_vwap(bar['vw'])
                print(f"Volume is {bar['v']}")
                global bars_df
                bars_df = bars_df.append(bar, ignore_index=True)
                stock.update_df(bars_df)

                # TODO: Once both vwap and rg conditions met, start cycle check for 2 green bars
                # TODO: build list of vwap tests or breaks with level of sharpness
            except TypeError:
                print(f"Type error")


    # [{"T":"b","S":"CVNA","o":11.53,"h":11.53,"l":11.53,"c":11.53,"v":230,"t":"2023-05-09T14:49:00Z","n":4,"vw":11.528913}]
def on_close(ws):
    print("closed connection")

socket = "wss://stream.data.alpaca.markets/v2/iex"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
