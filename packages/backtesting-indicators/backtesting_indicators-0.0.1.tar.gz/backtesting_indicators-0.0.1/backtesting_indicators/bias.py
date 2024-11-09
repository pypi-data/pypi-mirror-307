from backtesting._util import _Data
import pandas_ta as ta


def biasIndicator(data:_Data, length:int = 26, mamode:str = 'sma', drift:int = 1, offset:int = 0):
    """
    biasIndicator(data:_Data, length:int = 26, mamode:str = 'sma', drift:int = 1, offset:int = 0)
    
    Bias Indicator
    The Bias Indicator is a technical analysis tool that is used to gauge the bias of the market. It is based on the difference between the price and a moving average. The Bias Indicator is used to identify the direction of the market and to determine whether it is bullish or bearish.
    
    Args:
    data (_Data): Data
    length (int): Period
    mamode (str): Moving Average Mode
    drift (int): Drift
    offset (int): Offset
    
    Returns:
    pd.Series: New feature generated.
    """
    Close = data.Close

    attr = {
        'close': Close.s,
        'length': length,
        'mamode': mamode,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.bias(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = biasIndicator(data)
    print(data_indicator)
