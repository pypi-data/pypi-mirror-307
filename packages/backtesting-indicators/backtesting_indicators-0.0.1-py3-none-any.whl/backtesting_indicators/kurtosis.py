from backtesting._util import _Data
import pandas_ta as ta


def kurtosisIndicator(data:_Data, length:int = 30):
    """
    Kurtosis Indicator
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.kurtosis(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = kurtosisIndicator(data)
    print(data_indicator)