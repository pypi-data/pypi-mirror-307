from backtesting._util import _Data
import pandas_ta as ta


def zlmaIndicator(data:_Data, length:int = 10, mamode:str = 'ema', offset:int = 0, fillna = None, fill_method = None):
    """
    zlmaIndicator(data:_Data, length:int = 10, mamode:str = 'ema', offset:int = 0, fillna = None, fill_method = None)
    
    ZLEMA (Zero Lag Exponential Moving Average) is a moving average with zero lag. It is a fast and smooth moving average.
    
    params:
        - data: Data
        - length: int - default: 10
        - mamode: str - default: 'ema'
        - offset: int - default: 0
        - fillna: None
        - fill_method: None
        
    return:
        - pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'mamode': mamode,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.zlma(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = zlmaIndicator(data)
    print(data_indicator)