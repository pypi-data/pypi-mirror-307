from backtesting._util import _Data
import pandas_ta as ta


def swmaIndicator(data:_Data, length:int = 10, asc:bool = True, offset:int = 0, fillna = None, fill_method = None):
    """
    swmaIndicator(data:_Data, length:int = 10, asc:bool = True, offset:int = 0, fillna = None, fill_method = None)
    
    Simple Weighted Moving Average (SWMA)
    
    Simple Weighted Moving Average (SWMA) is a simple moving average that gives more weight to the price in the middle of a lookback period.
    
    Args:
    data : _Data : 
        Data
    length : int : 
        The period of the moving average
    asc : bool : 
        Direction of the moving average
    offset : int : 
        The offset of the moving average
    fillna : None : 
        Handle NaN values
    fill_method : None : 
        Handle NaN values
    
    Returns:
    SWMA : _Data : 
        New feature generated.
    """
    Close = data.Close

    def weights(w):
        def _compute(x):
            return np.dot(w * x)
        return _compute

    triangle = utils.symmetric_triangle(length - 1)
    SWMA = close.rolling(length)_.apply(weights(triangle), raw=True)

    return SWMA



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = swmaIndicator(data)
    print(data_indicator)
