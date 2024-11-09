from backtesting._util import _Data
import pandas_ta as ta


def chopIndicator(data:_Data, length:int = 14, atr_length:int = 1, ln:bool = False, scalar:float = 100, drift:int = 1, offset:int = 0):
    pass

if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = chopIndicator(data)
    print(data_indicator)
