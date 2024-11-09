from backtesting._util import _Data
import pandas_ta as ta


def log_returnIndicator(data:_Data, length:int = 20, cumulative:bool = False, offset:int = 0, fillna=None, fill_method=None):
    """
    log_returnIndicator(data:_Data, length:int = 20, cumulative:bool = False, offset:int = 0, fillna=None, fill_method=None)
    
    Log return indicator. Returns the log return of a time series.
    
    Args:
        data (_Data): dataset of values.
        length (int): period of the indicator.
        cumulative (bool): cumulative sum of the indicator.
        offset (int): offset of the indicator.
        fillna: data filling method.
        fill_method: filling method.
        
    Returns:
        pd.Series: New feature generated.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'cumulative': cumulative,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.log_return(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = log_returnIndicator(data)
    print(data_indicator)