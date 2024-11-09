from backtesting._util import _Data
import pandas_ta as ta


def t3Indicator(data:_Data, length:int = 10, a:float = 0.7):
    """
    t3Indicator(data:_Data, length:int = 10, a:float = 0.7)
    
    T3 Indicator
    
    Params:
    data: _Data : Data Object
    length: int : Length
    a: float : A
    
    Returns:
    rs: pd.Series : Result
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'a': a,
    }    
    
    rs = ta.t3(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = t3Indicator(data)
    print(data_indicator)