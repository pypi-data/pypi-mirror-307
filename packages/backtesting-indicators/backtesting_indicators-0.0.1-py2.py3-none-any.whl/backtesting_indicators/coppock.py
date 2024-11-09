from backtesting._util import _Data
import pandas_ta as ta


def coppockIndicator(data:_Data, length:int = 10, fast:int = 11, slow:int = 14):
    """
    coppockIndicator(data:_Data, length:int = 10, fast:int = 11, slow:int = 14)
    
    Coppock Curve
    The Coppock Curve is a momentum indicator that was developed by Edwin Coppock in 1962. 
    The indicator is designed for use on a monthly time scale. 
    It's the sum of a 14-month rate of change and 11-month rate of change, smoothed by a 10-period weighted moving average.
    
    Coppock Curve = 10-period WMA of 14-period RoC + 11-period RoC
    
    Parameters:
    data : _Data : 
        Data Object
    length : int : 10
        Length of the Coppock Curve
    fast : int : 11
        Fast Period
    slow : int : 14
        Slow Period
        
    Returns:
    rs : pd.Series
        Coppock Curve
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'fast': fast,
        'slow': slow,
    }    
    
    rs = ta.coppock(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = coppockIndicator(data)
    print(data_indicator)