from backtesting._util import _Data
import pandas_ta as ta


def pvolIndicator(data:_Data, signed:bool = True, offset:int = 0):
    """
    pvolIndicator(data:_Data, signed:bool = True, offset:int = 0)
    
    Price Volume Trend (PVT) is a cumulative indicator that uses volume and price to measure buying and selling pressure.
    
    Params:
    data : _Data : Data Object
    signed : bool : default is True
    offset : int : default is 0
    
    Returns:
    _Data : Data Object
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
        'signed': signed,
        'offset': offset,
    }    
    
    rs = ta.pvol(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pvolIndicator(data)
    print(data_indicator.df)