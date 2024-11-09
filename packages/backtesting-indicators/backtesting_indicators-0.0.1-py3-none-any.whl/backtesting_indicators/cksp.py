from backtesting._util import _Data
import pandas_ta as ta


def ckspIndicator(data:_Data, p:int = 10, x:float = 1, q:int = 9, tvmode:bool = True, offset:int = 0):
    """
    ckspIndicator(data:_Data, p:int = 10, x:float = 1, q:int = 9, tvmode:bool = True, offset:int = 0)
    
    CKSP Indicator
    
    CKSP is a momentum indicator that is used to identify the direction of the trend. It is based on the idea that the momentum of the price is the key to identifying the direction of the trend. The indicator is calculated by taking the difference between the closing price and the price of the previous day, and then dividing that difference by the closing price. The result is then multiplied by 100 to get a percentage value. The indicator is then plotted on a chart, with the values ranging from -100 to 100. A value of 100 indicates that the price is moving up, while a value of -100 indicates that the price is moving down.
    
    Parameters:
    - data: Data
    - p: int, default 10
    - x: float, default 1
    - q: int, default 9
    - tvmode: bool, default True
    - offset: int, default 0
    
    Returns:
    - rs: pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'p': p,
        'x': x,
        'q': q,
        'tvmode': tvmode,
        'offset': offset,
    }    
    
    rs = ta.cksp(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ckspIndicator(data)
    print(data_indicator)
