from backtesting._util import _Data
import pandas_ta as ta


def natrIndicator(data:_Data, length:int = 20, scalar:float = 100, mamode:str = 'ema', talib:bool = True, offset:int = 0, fillna=None, fill_method=None):
    """
    natrIndicator(data:_Data, length:int = 20, scalar:float = 100, mamode:str = 'ema', talib:bool = True, offset:int = 0, fillna=None, fill_method=None)
    
    Normalized Average True Range (NATR) is a measure of volatility. It is similar to ATR but NATR normalizes the values to be between 0 and 100.
    
    Args:
    data (_Data): The pandas DataFrame object with the data.
    length (int): The time period. Default: 20
    scalar (float): A positive floating point value. Default: 100
    mamode (str): The moving average mode. Default: 'ema'
    talib (bool): If True, uses talib. Default: True
    offset (int): How many periods to offset the result. Default: 0
    fillna: How to handle NaN values. Default: None
    fill_method: 'ffill' or 'bfill'. Default: None
    
    Returns:
    pandas Series: NATR
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'scalar': scalar,
        'mamode': mamode,
        'talib': talib,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method
    }
    
    rs = ta.natr(**attr)
    
    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = natrIndicator(data)
    print(data_indicator)
