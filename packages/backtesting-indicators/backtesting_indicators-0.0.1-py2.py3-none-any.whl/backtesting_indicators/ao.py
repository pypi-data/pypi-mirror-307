from backtesting._util import _Data
import pandas_ta as ta


def aoIndicator(data:_Data, fast:int = 5, slow:int = 34, offset:int = 0, fillna = None, fill_method = None):
    """
    Awesome Oscillator (AO)
    
    The Awesome Oscillator is an indicator used to measure market momentum. AO calculates the difference of a 34 Period and 5 Period Simple Moving Averages. The Simple Moving Averages that are used are not calculated using closing price but rather each bar's midpoints. AO is generally used to affirm trends or to anticipate possible reversals.
    
    Args:
    data : _Data : 
        data object
    fast : int : 5
        The short period. Default: 5
    slow : int : 34
        The long period. Default: 34
    offset : int : 0
        How many periods to offset the result. Default: 0
    fillna : int : None
        How to handle NaN values. Default: None
    fill_method : str : None
        'ffill' or 'bfill'. Default: None
    
    Returns:
    _Data
    """
    high = data.High
    low = data.Low
    
    attr = {
        'high': high.s,
        'low': low.s,
        'fast': fast,
        'slow': slow,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method
    }
    
    rs = ta.ao(**attr)
    
    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = aoIndicator(data)
    print(data_indicator)
    import matplotlib.pyplot as plt
    plt.plot(data_indicator)
    plt.show()