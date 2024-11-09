from backtesting._util import _Data
import pandas_ta as ta


def decreasingIndicator(data:_Data, length:int = 1, strict:bool = False, percent:float = None, asint:bool = True, drift:int = 1, offset:int = 0):
    """
    decreasingIndicator(data:_Data, length:int = 1, strict:bool = False, percent:float = None, asint:bool = True, drift:int = 1, offset:int = 0)
    
    Decreasing indicator
    
    Params:
    -------
    data : _Data
        Data
    length : int
        Length
    strict : bool
        Strict
    percent : float
        Percent
    asint : bool
        Asint
    drift : int
        Drift
    offset : int
        Offset
        
    Returns:
    --------
    pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'strict': strict,
        'percent': percent,
        'asint': asint,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.decreasing(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = decreasingIndicator(data)
    print(data_indicator)
