from backtesting._util import _Data
import pandas_ta as ta


def cmfIndicator(data:_Data, length:int = 20, open_:pd.Series = None):
    """
    Chaikin Money Flow Indicator
    The Chaikin Money Flow (CMF) is an indicator that measures the amount of money flow volume over a specific period. 
    It is used to determine buying and selling pressure.
    
    Parameters:
    data: _Data
        Data with High, Low, Close and Volume
    length: int
        Period to calculate the indicator
    open_: pd.Series
        Open prices
    
    Returns:
    CMF: pd.Series
        Chaikin Money Flow Indicator
    """
    high = data.High
    low = data.Low
    close = data.Close
    volume = data.Volume
    
    if open_ is not None:
        ad = close - open_
    else:
        ad = 2 * close - high - low

    hl_range = high - low
    ad = ad * volume / hl_range
    CMF = ad.rolling(length).sum() / volume.rolling(length).sum()
    
    return CMF


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cmfIndicator(data)
    print(data_indicator)