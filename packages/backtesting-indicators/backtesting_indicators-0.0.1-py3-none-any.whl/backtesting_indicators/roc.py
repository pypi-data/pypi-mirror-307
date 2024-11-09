from backtesting._util import _Data
import pandas_ta as ta


def rocIndicator(data:_Data, length:int = 1, scalar:float = 100, talib:bool = True, offset:int = 0, fillna=None, fill_method=None):
    """
    rocIndicator(data:_Data, length:int = 1, scalar:float = 100, talib:bool = True, offset:int = 0, fillna=None, fill_method=None)
    
    Rate of Change (ROC)
    
    The Rate-of-Change (ROC) indicator, which is also referred to as simply Momentum, is a pure momentum oscillator that measures the percent change in price from one period to the next. The ROC calculation compares the current price with the price ânâ periods ago.
    
    ROC = [(Close - Close n periods ago) / (Close n periods ago)] * 100
    
    Parameters:
    data : _Data : 
        Data Object
    length : int : 1
        ROC period
    scalar : float : 100
        scalar
    talib : bool : True
        If True, use talib
    offset : int : 0
        How many periods to offset the result
    fillna : any : None
        fillna
    fill_method : any : None
        fill_method
    
    Returns:
    pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'scalar': scalar,
        'talib': talib,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method
    }    
    
    rs = ta.roc(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = rocIndicator(data)
    print(data_indicator)