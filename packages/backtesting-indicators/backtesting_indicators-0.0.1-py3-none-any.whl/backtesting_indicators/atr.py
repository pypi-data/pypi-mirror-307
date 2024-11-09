from backtesting._util import _Data
import pandas_ta as ta


def atrIndicator(data:_Data, length:int = 14, mamode:str = 'rma', talib:bool = True, drift:int = 1, percent:bool = False, offset:int = 0, fillna = None, fill_method = None):
    """
    atrIndicator(data:_Data, length:int = 14, mamode:str = 'rma', talib:bool = True, drift:int = 1, percent:bool = False, offset:int = 0, fillna = None, fill_method = None)
    
    Average True Range (ATR)
    
    Average True Range is a volatility indicator that shows how much an asset moves, on average, during a given time frame. The indicator can help day traders confirm when they might want to initiate a trade, and it can be used to determine the placement of a stop-loss order.
    
    Source:
    https://www.investopedia.com/terms/a/atr.asp
    
    Params:
    data : _Data : 
        data object
    length : int : 14
        Number of period
    mamode : str : 'rma'
        ma mode
    talib : bool : True
        use talib
    drift : int : 1
        drift
    percent : bool : False
        percent
    offset : int : 0
        offset
    fillna : None
        fillna
    fill_method : None
        fill method
    
    Returns:
    _Data
        new 'atr' column
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'mamode': mamode,
        'talib': talib,
        'drift': drift,
        'percent': percent,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method
    }
    
    rs = ta.atr(**attr)
    
    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = atrIndicator(data)
    print(data_indicator.df)