import datetime
from backtesting_data.history import historySymbol
from backtesting_indicators.aberration import aberrationIndicator
from backtesting._util import _Data

tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
data = _Data(tmp)
data_indicator = aberrationIndicator(data)
print(data_indicator)