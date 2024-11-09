from backtesting._util import _Data
import pandas_ta as ta


def amatIndicator(data:_Data, length:int = 10):
    """
    AMA (Adaptive Moving Average) Indicator
    AMA is a moving average that adapts to the market volatility.
    It is a fast-responding moving average that is more closely
    associated with price changes than a simple moving average.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.amat(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = amatIndicator(data)
    print(data_indicator)