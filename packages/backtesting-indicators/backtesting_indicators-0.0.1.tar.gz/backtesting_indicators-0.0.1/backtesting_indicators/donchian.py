from backtesting._util import _Data
import pandas_ta as ta


def donchianIndicator(data:_Data, lower_length:int = 20, upper_length:int = 20, offset:int = 0):
    """
    Donchian Channel Indicator
    :param data: Data
    :param lower_length: int
    :param upper_length: int
    :param offset: int
    :return: pd.Series
    """
    high = data.High
    low = data.Low
    
    attr = {
        'high': high.s,
        'low': low.s,
        'lower_length': lower_length,
        'upper_length': upper_length,
        'offset': offset,
    }    
    
    rs = ta.donchian(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = donchianIndicator(data)
    print(data_indicator)