from backtesting._util import _Data
import pandas_ta as ta


def uiIndicator(data:_Data, length:int = 14, scalar:float = 100, everget:bool = False):
    """
    uiIndicator(data:_Data, length:int = 14, scalar:float = 100, everget:bool = False)
    
    UI Indicator
    
    Params:
    data:_Data: Data
    length:int: Length
    scalar:float: Scalar
    everget:bool: Everget
    
    Returns:
    rs: pd.Series
    """
    High = data.High
    Close = data.Close
    
    attr = {
        'high': High.s,
        'close': Close.s,
        'length': length,
        'scalar': scalar,
        'everget': everget,
    }    
    
    rs = ta.ui(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = uiIndicator(data)
    print(data_indicator)