from backtesting._util import _Data
import pandas_ta as ta


def aroonIndicator(data:_Data, length:int = 14, scalar:float = 100, talib:bool = True, offset:int = 0, fillna:float = None, fill_method:str = None):
    """
    aroonIndicator(data:_Data, length:int = 14, scalar:float = 100, talib:bool = True, offset:int = 0, fillna:float = None, fill_method:str = None)
    
    Aroon Indicator
    Identifies the trend direction and strength.
    
    Params:
    data: _Data
    length: int - default: 14
    scalar: float - default: 100
    talib: bool - default: True
    offset: int - default: 0
    fillna: float - default: None
    fill_method: str - default: None
    
    Returns:
    rs: pd.Series
    """
    Close = data.Close
    High = data.High
    Low = data.Low
    
    attr = {
        'close': Close.s,
        'length': length,
        'scalar': scalar,
        'talib': talib,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.aroon(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = aroonIndicator(data)
    print(data_indicator)