from backtesting._util import _Data
import pandas_ta as ta


def rvgiIndicator(data:_Data, length:int = 14, swma_length:int = 4, offset:int = 0):
    """
    data: _Data
    length: int = 14
    swma_length: int = 4
    offset: int = 0
    """
    open_ = data.Open
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'open_': open_.s,
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'swma_length': swma_length,
        'offset': offset,
    }    
    
    rs = ta.rvgi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = rvgiIndicator(data)
    print(data_indicator)