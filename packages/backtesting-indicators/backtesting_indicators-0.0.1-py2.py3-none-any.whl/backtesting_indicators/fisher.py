from backtesting._util import _Data
import pandas_ta as ta


def fisherIndicator(data:_Data, length:int = 9, signal:int = 1):
    """
    Fisher Indicator
    :param data: Data
    :param length: int = 9
    :param signal: int = 1
    :return: pd.Series
    """
    High = data.High
    Low = data.Low
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'length': length,
        'signal': signal,
    }    
    
    rs = ta.fisher(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = fisherIndicator(data)
    print(data_indicator)