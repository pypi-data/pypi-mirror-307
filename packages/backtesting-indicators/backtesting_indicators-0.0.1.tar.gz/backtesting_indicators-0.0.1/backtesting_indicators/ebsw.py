from backtesting._util import _Data
import pandas_ta as ta


def ebswIndicator(data:_Data, length:int = 40, bars:int = 10, drift:int = 1, offset:int = 0):
    """
    ebswIndicator(data:_Data, length:int = 40, bars:int = 10, drift:int = 1, offset:int = 0)
    
    Exponential Bollinger Bands Width (EBSW) is a volatility indicator that measures the difference between the upper and lower Bollinger Bands.
    
    Params:
    - data: Data
    - length: int = 40
    - bars: int = 10
    - drift: int = 1
    - offset: int = 0
    
    Returns:
    - rs: Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'bars': bars,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.ebsw(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ebswIndicator(data)
    print(data_indicator)
