from backtesting._util import _Data
import pandas_ta as ta


def qqeIndicator(data:_Data, length:int = 14, smooth:int = 5, factor:float = 4.236, mamode:str = 'sma', drift:int = 1, offset:int = 0):
    """
    QQE Indicator
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'smooth': smooth,
        'factor': factor,
        'mamode': mamode,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.qqe(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = qqeIndicator(data)
    print(data_indicator)