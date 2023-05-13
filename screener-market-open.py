import stock_utils
from datetime import datetime, timedelta

TICKER_SYMBOLS = ['AI', 'CXAI', 'MARA', 'DPST', 'IMGN']

for ticker in TICKER_SYMBOLS:
    stock_utils.get_market_open_probability(ticker, 10)

# AI - Probability of market open perk: 50.00% with avg delta of $0.28 -- open 17.42, close 17.3 ($.12 DOWN)
# CXAI - Probability of market open perk: 57.14% with avg delta of $0.99 -- open 11.28, close 10.8 ($.48 DOWN)
# MARA - Probability of market open perk: 57.14% with avg delta of $0.20 -- open 9.79, close 9.72 ($.07 DOWN)
# DPST - Probability of market open perk: 64.29% with avg delta of $0.12 -- open 4.26, close 4.04 ($.22 DOWN
# IMGN - Probability of market open perk: 71.43% with avg delta of $0.17 -- open 12.46, close 12.91 ($.45 UP)
