from backtesting._util import _Data
import pandas_ta as ta


def kcIndicator(data:_Data, length:int = 20, scalar:float = 2, mamode:str = None, tr:bool = True):
    """
    kcIndicator(data:_Data, length:int = 20, scalar:float = 2, mamode:str = None, tr:bool = True)
    
    Keltner Channels (KC) indicator
    
    Params:
    data : _Data : Data
    length : int : Period
    scalar : float : Scalar
    mamode : str : MA mode
    tr : bool : True
    
    Returns:
    _Data : Data
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
        'tr': tr,
    }    
    
    rs = ta.kc(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = kcIndicator(data)
    print(data_indicator.df)