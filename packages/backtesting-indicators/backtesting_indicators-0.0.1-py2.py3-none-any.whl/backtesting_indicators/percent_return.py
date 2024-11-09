from backtesting._util import _Data
import pandas_ta as ta


def percent_returnIndicator(data:_Data, length:int = 20, cumulative:bool = False, offset:int = 0, fillna=None, fill_method=None):
    """
    percent_returnIndicator(data:_Data, length:int = 20, cumulative:bool = False, offset:int = 0, fillna=None, fill_method=None)
    
    Percent Return Indicator
    The Percent Return Indicator calculates the percentage return of a time series.
    
    Args:
        data (_Data): Dataset
        length (int): The number of periods to look back.
        cumulative (bool): If True, returns the cumulative percentage return.
        offset (int): The offset of the indicator. Default: 0
        fillna (value, optional): The value to use for the initial periods. Default: None
        fill_method (value, optional): The fill method for the initial periods. Default: None
        
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
        'fill_method': fill_method
    }    
    
    rs = ta.percent_return(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = percent_returnIndicator(data)
    print(data_indicator)