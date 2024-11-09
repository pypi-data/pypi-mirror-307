from backtesting._util import _Data
import pandas_ta as ta


def almaIndicator(data:_Data, length:int = 10, sigma:float = 6.0, distribution_offset:float = 0.85, offset:int = 0):
    '''
    almaIndicator(data:_Data, length:int = 10, sigma:float = 6.0, distribution_offset:float = 0.85, offset:int = 0)
    
    ALMA (Arnaud Legoux Moving Average) is a moving average based on a variable length moving average. 
    The length of the moving average and the offset are controlled by the input parameters. 
    The moving average is calculated as the sum of the product of the data and a weighting function. 
    The weighting function is a Gaussian distribution. 
    The distribution_offset parameter controls the offset of the distribution. 
    The sigma parameter controls the width of the distribution. 
    The offset parameter controls the center of the distribution.
    
    Args:
        data (_Data): Dataset
        length (int): Number of periods
        sigma (float): Width of the distribution
        distribution_offset (float): Offset of the distribution
        offset (int): Center of the distribution
    
    Returns:
        rs (pd.Series): Resulting values
    '''
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'sigma': sigma,
        'distribution_offset': distribution_offset,
        'offset': offset,
    }    
    
    rs = ta.alma(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = almaIndicator(data)
    print(data_indicator)