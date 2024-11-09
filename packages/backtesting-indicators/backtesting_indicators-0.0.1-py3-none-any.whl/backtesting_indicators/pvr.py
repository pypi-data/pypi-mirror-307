from backtesting._util import _Data
import pandas_ta as ta


def pvrIndicator(data:_Data):
    """
    data: _Data
    return: pd.Series
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
    }    
    
    rs = ta.pvr(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pvrIndicator(data)
    print(data_indicator)