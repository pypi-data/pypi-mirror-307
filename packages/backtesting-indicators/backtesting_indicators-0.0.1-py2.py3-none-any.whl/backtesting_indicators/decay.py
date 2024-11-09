from backtesting._util import _Data
import pandas_ta as ta


def decayIndicator(data:_Data, length:int = 5, mode:str = None, offset:int = 0):
    """
    decayIndicator(data:_Data, length:int = 5, mode:str = None, offset:int = 0)
    
    Decay
    
    Decay is a weighted moving average that gives more weight to more recent prices. The result is a curve that follows the price trend more closely than a simple moving average. Decay is also known as Exponential Moving Average.
    
    Args:
        data (_Data): The object of the data.
        length (int): The number of periods to use in the calculation.
        mode (str): The mode of the moving average. It can be one of the following: 'linear', 'exponential', 'wilder', 'weighted', 'simple'.
        offset (int): The number of periods to offset the result. A positive offset moves the result into the past.
    
    Returns:
        pd.Series: The decay indicator.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'mode': mode,
        'offset': offset,
    }    
    
    rs = ta.decay(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = decayIndicator(data)
    print(data_indicator)
