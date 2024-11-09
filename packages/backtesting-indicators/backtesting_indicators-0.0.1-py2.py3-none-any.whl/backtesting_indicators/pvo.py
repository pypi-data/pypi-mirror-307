from backtesting._util import _Data
import pandas_ta as ta


def pvoIndicator(data:_Data, fast:int = 12, slow:int = 26, signal:int = 9, scalar:float = 100, offset:int = 0):
    """
    pvoIndicator(data:_Data, fast:int = 12, slow:int = 26, signal:int = 9, scalar:float = 100, offset:int = 0)
    
    PVO - Percentage Volume Oscillator
    The Percentage Volume Oscillator (PVO) is a momentum oscillator for volume. PVO measures the difference between two volume-based moving averages as a percentage of the larger moving average.
    
    Args:
    data : _Data : Dataset
    fast : int : The short period. Default: 12
    slow : int : The long period. Default: 26
    signal : int : The signal period. Default: 9
    scalar : float : A constant to multiply the result. Default: 100
    offset : int : How many periods to offset the result. Default: 0
    
    Returns:
    rs : pd.Series
    """
    Volume = data.Volume
    
    attr = {
        'volume': Volume.s,
        'fast': fast,
        'slow': slow,
        'signal': signal,
        'scalar': scalar,
        'offset': offset,
    }    
    
    rs = ta.pvo(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pvoIndicator(data)
    print(data_indicator)