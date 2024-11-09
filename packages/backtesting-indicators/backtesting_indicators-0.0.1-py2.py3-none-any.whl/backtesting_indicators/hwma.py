from backtesting._util import _Data
import pandas_ta as ta


def hwmaIndicator(data:_Data, na:float = 0.2, nb:float = 0.1, nc:float = 0.1):
    """
    hwmaIndicator(data:_Data, na:float = 0.2, nb:float = 0.1, nc:float = 0.1)
    
    Hull Moving Average (HMA) is a technical indicator that helps to identify the trend of the market. 
    It is based on weighted moving averages and eliminates lag. 
    The HMA gives the direction of the trend and works better on long-term charts.
    
    Params:
    data: Data
    na: float
    nb: float
    nc: float
    
    Returns:
    rs: Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'na': na,
        'nb': nb,
        'nc': nc,
    }    
    
    rs = ta.hwma(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = hwmaIndicator(data)
    print(data_indicator)