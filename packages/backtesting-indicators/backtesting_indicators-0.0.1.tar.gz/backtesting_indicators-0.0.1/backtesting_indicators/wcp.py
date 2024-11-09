from backtesting._util import _Data
import pandas_ta as ta


def wcpIndicator(data:_Data):
    """
    data: _Data
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
    }    
    
    rs = ta.wcp(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = wcpIndicator(data)
    print(data_indicator)