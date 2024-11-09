from backtesting._util import _Data
import pandas_ta as ta


def vortexIndicator(data:_Data, length:int = 14, drift:int = 1, offset:int = 0):
    """
    Vortex Indicator
    Formula:
    tr = ta.tr(high, low, close)
    tr_sum = tr.rolling(length).sum()
    
    vmp = (high - low.shift(drift)).abs()
    vmn = (low - high.shift(drift)).abs()
    
    VIP = vmp.rolling(length).sum() / tr_sum
    VIM = vmn.rolling(length).sum() / tr_sum
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    tr = ta.tr(high, low, close)
    tr_sum = tr.rolling(length).sum()
    
    vmp = (high - low.shift(drift)).abs()
    vmn = (low - high.shift(drift)).abs()
    
    VIP = vmp.rolling(length).sum() / tr_sum
    VIM = vmn.rolling(length).sum() / tr_sum
    
    return VIP, VIM


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = vortexIndicator(data)
    print(data_indicator)