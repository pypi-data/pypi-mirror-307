from backtesting._util import _Data
import pandas_ta as ta


def ppoIndicator(data:_Data, fast:int = 12, slow:int = 26, signal:int = 9, scalar:float = 100, mamode:str = 'sma', talib:bool = True, offset:int = 0, fillna:float = None, fill_method:str = None):
    """
    ppoIndicator(data:_Data, fast:int = 12, slow:int = 26, signal:int = 9, scalar:float = 100, mamode:str = 'sma', talib:bool = True, offset:int = 0, fillna:float = None, fill_method:str = None)
    
    PPO - Percentage Price Oscillator
    
    Returns:
    Series: New feature generated.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'fast': fast,
        'slow': slow,
        'signal': signal,
        'scalar': scalar,
        'mamode': mamode,
        'talib': talib,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.ppo(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ppoIndicator(data)
    print(data_indicator)