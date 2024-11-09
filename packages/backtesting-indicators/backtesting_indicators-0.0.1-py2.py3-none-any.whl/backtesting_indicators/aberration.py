from backtesting._util import _Data
import pandas_ta as ta


def aberrationIndicator(data:_Data, length:int = 5, atr_length:int = 15, offset:int = 0):
    """
    aberrationIndicator(data:_Data, length:int = 5, atr_length:int = 15, offset:int = 0)
    
    Aberration Indicator
    The Aberration Indicator is a price band that is used to gauge the market's volatility. The upper band is calculated by adding the moving average of the high and low prices to the closing price. The lower band is calculated by subtracting the moving average of the high and low prices from the closing price. The bands are plotted at a set number of standard deviations around a moving average.
    
    Args:
        data (_Data): Data
        length (int): Number of periods to calculate the indicator
        atr_length (int): Number of periods to calculate the Average True Range
        offset (int): Offset
        
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
        'atr_length': atr_length,
        'offset': offset,
    }    
    
    rs = ta.aberration(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = aberrationIndicator(data)
    print(data_indicator)