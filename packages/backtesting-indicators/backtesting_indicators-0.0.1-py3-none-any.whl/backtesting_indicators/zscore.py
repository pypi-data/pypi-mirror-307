from backtesting._util import _Data
import pandas_ta as ta


def zscoreIndicator(data:_Data, length:int = 30, std:float = 1, offset:int = 0):
    """
    zscoreIndicator(data:_Data, length:int = 30, std:float = 1, offset:int = 0)
    
    Z-Score Indicator
    
    Args:
    data (_Data): Data Class
    length (int): Period
    std (float): Standard Deviation
    offset (int): Offset
    
    Returns:
    rs (pd.Series): Result
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'std': std,
        'offset': offset,
    }    
    
    rs = ta.zscore(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = zscoreIndicator(data)
    print(data_indicator)