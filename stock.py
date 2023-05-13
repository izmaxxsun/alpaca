import stock_utils
from ta.volume import VolumeWeightedAveragePrice
class Stock:

    def __init__(self, symbol):
        self.latest_close_timestamp = None
        self.symbol = symbol
        self.prev_close = self.get_previous_close()
        self.latest_close = self.prev_close
        self.latest_vwap = None
        self.is_above_rg = False
        self.is_above_vw = False
        self.dataframe = None

    def update_df(self, bars_df):
        self.dataframe = bars_df
        self.vwap()
        print(f"Self df is\n: {self.dataframe}")

    def get_previous_close(self):
        stock_snapshot_dict = stock_utils.get_stock_snapshot(self.symbol)
        # print(stock_snapshot_dict)
        stock_snapshot = stock_snapshot_dict.get(self.symbol)
        prev_daily_bar = stock_snapshot.previous_daily_bar
        prev_close = prev_daily_bar.close

        return prev_close

    def update_latest_close(self, close_price):
        self.latest_close = close_price
        rg_delta = self.latest_close - self.prev_close

        if rg_delta > 0:
            self.is_above_rg = True
        else:
            self.is_above_rg = False

        print(f"R/G delta is ${rg_delta:.2f} and above RG is {self.is_above_rg}")

    def update_latest_vwap(self, vwap):
        # TODO: create own vwap calc, the Alpaca one isn't right
        # https://stackoverflow.com/questions/44854512/how-to-calculate-vwap-volume-weighted-average-price-using-groupby-and-apply

        self.latest_vwap = vwap
        vwap_delta = self.latest_close - self.latest_vwap

        if vwap_delta > 0:
            self.is_above_vw = True
        else:
            self.is_above_vw = False

        print(f"VWAP delta is ${vwap_delta:.2f} and above VWAP is {self.is_above_vw}")

    def vwap(self, label='vwap', window=3, fillna=True):
        self.dataframe[label] = VolumeWeightedAveragePrice(high=self.dataframe['h'], low=self.dataframe['l'],
                                                      close=self.dataframe["c"], volume=self.dataframe['v'],
                                                      window=window, fillna=fillna).volume_weighted_average_price()

