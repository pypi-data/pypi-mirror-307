from backtesting._util import _Data
import pandas_ta as ta


def mcgdIndicator(data:_Data, length:int = 10, offset:int = 0, c:float = 1):
    """
    mcgdIndicator(data:_Data, length:int = 10, offset:int = 0, c:float = 1)
    
    Moving Center of Gravity Divergence Indicator
    
    Params:
    data: _Data
    length: int - default: 10
    offset: int - default: 0
    c: float - default: 1
    
    Returns:
    pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'offset': offset,
        'c': c
    }    
    
    rs = ta.mcg(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = mcgdIndicator(data)
    print(data_indicator)