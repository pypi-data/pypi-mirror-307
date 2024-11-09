from backtesting._util import _Data
import pandas_ta as ta


def eriIndicator(data:_Data, length:int = 13):
    """
    ERI - Elder Ray Index
    Formula:
    ERI = (Close - SMA(High, length)) / (SMA(High, length) - SMA(Low, length))
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.eri(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = eriIndicator(data)
    print(data_indicator)