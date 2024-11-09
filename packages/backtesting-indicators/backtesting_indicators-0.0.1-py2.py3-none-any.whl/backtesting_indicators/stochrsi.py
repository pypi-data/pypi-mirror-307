from backtesting._util import _Data
import pandas_ta as ta


def stochrsiIndicator(data:_Data, length:int = 14, rsi_length:int = 14, k:int = 3, d:int = 3, mamode:str = 'sma', offset:int = 0):
    """
    stochrsiIndicator(data:_Data, length:int = 14, rsi_length:int = 14, k:int = 3, d:int = 3, mamode:str = 'sma', offset:int = 0)
    
    Stochastic RSI (StochRSI) is a momentum oscillator, which measures both the RSI value and the Stochastic value.
    
    Args:
    data (_Data): Dataset.
    length (int): Period for StochRSI.
    rsi_length (int): Period for RSI.
    k (int): Period for %K.
    d (int): Period for %D.
    mamode (str): Moving average mode.
    offset (int): Offset value.
    
    Returns:
    pd.Series: New feature generated.
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
        'rsi_length': rsi_length,
        'k': k,
        'd': d,
        'mamode': mamode,
        'offset': offset,
    }    
    
    rs = ta.stochrsi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = stochrsiIndicator(data)
    print(data_indicator)