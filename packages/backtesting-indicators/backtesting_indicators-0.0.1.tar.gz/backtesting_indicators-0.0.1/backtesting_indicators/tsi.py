from backtesting._util import _Data
import pandas_ta as ta


def tsiIndicator(data:_Data, fast:int = 13, slow:int = 25, signal:int = 13, scalar:float = 100, drift:int = 1, mamode:str = 'ema', offset:int = 0, fillna:float = None, fill_method:str = None):
    """
    tsiIndicator(data:_Data, fast:int = 13, slow:int = 25, signal:int = 13, scalar:float = 100, drift:int = 1, mamode:str = 'ema', offset:int = 0, fillna:float = None, fill_method:str = None)
    
    True Strength Index (TSI)
    
    The True Strength Index (TSI) is a momentum-based indicator, developed by William Blau. TSI is a
    momentum oscillator based on a double smoothing of price changes. TSI is calculated by using the
    price changes of the underlying asset, while also taking into account the price changes of the asset's
    price momentum.
    
    TSI = 100 * (PC / ABS(ABS(PC)))
    
    Where:
    PC = Double smoothed price change
    ABS = Absolute Value
    
    TSI is often used to determine overbought or oversold conditions in a market, as well as to identify
    trend strength and direction. TSI can be used on any asset and across any time frame.
    
    Source:
    https://www.tradingview.com/wiki/True_Strength_Index_(TSI)
    
    Params:
    data : _Data : 
        data object
    fast : int : 13
        fast period
    slow : int : 25
        slow period
    signal : int : 13
        signal period
    scalar : float : 100
        scalar
    drift : int : 1
        drift
    mamode : str : 'ema'
        ma mode
    offset : int : 0
        shift
    fillna : float : None
        fillna
    fill_method : str : None
        fill method
    
    Returns:
    rs : pd.Series
        tsi
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'fast': fast,
        'slow': slow,
        'signal': signal,
        'scalar': scalar,
        'mamode': mamode,
        'drift': drift,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.tsi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = tsiIndicator(data)
    print(data_indicator)