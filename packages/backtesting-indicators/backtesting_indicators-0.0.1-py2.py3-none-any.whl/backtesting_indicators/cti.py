from backtesting._util import _Data
import pandas_ta as ta


def ctiIndicator(data:_Data, length:int = 12, offset:int = 0):
    """
    ctiIndicator(data:_Data, length:int = 12, offset:int = 0)
    
    Commodity Channel Index (CCI) measures the difference between the typical price of a commodity and its simple moving average, 
    expressed as an index either above or below zero. 
    It is an unbounded oscillator that generally fluctuates between +100 and -100. 
    The CCI can be used to determine overbought and oversold levels.
    
    Args:
        data (_Data): Data
        length (int): Number of period
        offset (int): Offset value
        
    Returns:
        _Data: Result
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'offset': offset,
    }    
    
    rs = ta.cti(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ctiIndicator(data)
    print(data_indicator)
    print(data_indicator.df)