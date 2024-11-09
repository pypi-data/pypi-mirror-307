from backtesting._util import _Data
import pandas_ta as ta


def vidyaIndicator(data:_Data, length:int = 10, adjust:bool = False, sma:bool = True, talib:bool = True, fillna=None, fill_method=None):
    """
    vidyaIndicator(data:_Data, length:int = 10, adjust:bool = False, sma:bool = True, talib:bool = True, fillna=None, fill_method=None)
    
    VIDYA (Variable Index Dynamic Average) is a moving average that automatically adjusts its smoothing constant based on market volatility.
    
    Params:
    data: Data
    length: int - default: 10
    adjust: bool - default: False
    sma: bool - default: True
    talib: bool - default: True
    fillna: None
    fill_method: None
    
    Returns:
    rs: pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'adjust': adjust,
        'sma': sma,
        'talib': talib,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.vidya(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = vidyaIndicator(data)
    print(data_indicator)