from backtesting._util import _Data
import pandas_ta as ta

def varianceIndicator(data:_Data, length:int = 30, ddof:int = 0, talib:bool = True, offset:int = 0):
    """
    varianceIndicator(data:_Data, length:int = 30, ddof:int = 0, talib:bool = True, offset:int = 0)
    
    Variance Indicator
    Inputs:
        data: _Data
        length: int = 30
        ddof: int = 0
        talib: bool = True
        offset: int = 0
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'ddof': ddof,
        'talib': talib,
        'offset': offset,
    }    
    
    rs = ta.variance(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = varianceIndicator(data)
    print(data_indicator)