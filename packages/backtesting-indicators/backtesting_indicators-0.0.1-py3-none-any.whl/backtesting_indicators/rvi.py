from backtesting._util import _Data
import pandas_ta as ta


def rviIndicator(data:_Data, length:int = 14, scalar:float = 100, refined:bool = False, thirds:bool = False, mamode:str = 'ema', offset:int = 0):
    """
    rviIndicator(data:_Data, length:int = 14, scalar:float = 100, refined:bool = False, thirds:bool = False, mamode:str = 'ema', offset:int = 0)
    
    Relative Volatility Index (RVI) is a volatility indicator that was developed by Donald Dorsey to indicate the direction of volatility. 
    RVI is the Relative Volatility Index and is calculated in the following way:
    
    RVI = (SMA(High - Low, length) / SMA(High + Low, length)) * scalar
    
    Parameters:
    data : _Data : 
        Data Object
    length : int : 14
        The number of periods to use in the calculation.
    scalar : float : 100
        A scalar to multiply the result by.
    refined : bool : False
        If True, the RVI will be refined.
    thirds : bool : False
        If True, the RVI will be divided into thirds.
    mamode : str : 'ema'
        The moving average mode to use in the calculation.
    offset : int : 0
        The offset to use in the calculation.
    
    Returns:
    _Data : 
        A new data object with the RVI values.
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
        'refined': refined,
        'thirds': thirds,
        'mamode': mamode,
        'offset': offset,
    }    
    
    rs = ta.rvi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = rviIndicator(data)
    print(data_indicator.df)