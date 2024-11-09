from backtesting._util import _Data
import pandas_ta as ta


def crossIndicator(data:_Data, a, b):
    """
    data: _Data
    a: Indicator
    b: Indicator
    """
    attr = {
        'a': a.s,
        'b': b.s,
    }
    rs = ta.cross(**attr)
    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = crossIndicator(data, ta.ema(data, 5), ta.ema(data, 10))
    print(data_indicator)
    print(data_indicator.tail(10))