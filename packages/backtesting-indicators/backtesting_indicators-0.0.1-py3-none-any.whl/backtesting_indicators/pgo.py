from backtesting._util import _Data
import pandas_ta as ta


def pgoIndicator(data:_Data, length:int = 14):
    """
    pgoIndicator(data:_Data, length:int = 14)
    
    PGO - Pretty Good Oscillator
    
    PGO is a momentum indicator that measures the distance between the price and the moving average.
    The PGO is calculated as the difference between the price and the moving average, divided by the moving average.
    The PGO is then smoothed using a moving average.
    
    Args:
    data (_Data): The data to use in the calculation.
    length (int): The length of the moving average.
    
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
    }    
    
    rs = ta.pgo(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pgoIndicator(data)
    print(data_indicator)
