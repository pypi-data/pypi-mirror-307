from backtesting._util import _Data
import pandas_ta as ta


def bopIndicator(data:_Data, scalar:float = 1, talib:bool = True, offset:int = 0):
    """
    bopIndicator(data:_Data, scalar:float = 1, talib:bool = True, offset:int = 0)
    
    BOP (Balance of Power) indicator
    
    Params:
    data: _Data : Data
    scalar: float : Scalar
    talib: bool : Ta-lib
    offset: int : Offset
    
    Returns:
    rs : _Data : Data
    """
    Open = data.Open
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'open': Open.s,
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'scalar': scalar,
        'talib': talib,
        'offset': offset,
    }    
    
    rs = ta.bop(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = bopIndicator(data)
    print(data_indicator.df)