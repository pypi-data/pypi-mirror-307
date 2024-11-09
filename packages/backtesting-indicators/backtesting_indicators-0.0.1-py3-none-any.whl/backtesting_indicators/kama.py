from backtesting._util import _Data
import pandas_ta as ta


def kamaIndicator(data:_Data, length:int = 10, fast:int = 2, slow:int = 30, drift:int = 1, offset:int = 0):
    """
    data: _Data
    length: int = 10
    fast: int = 2
    slow: int = 30
    drift: int = 1
    offset: int = 0
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'fast': fast,
        'slow': slow,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.kama(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = kamaIndicator(data)
    print(data_indicator)