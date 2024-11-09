from backtesting._util import _Data
import pandas_ta as ta


def skewIndicator(data:_Data, length:int = 30, offset:int = 0, fillna = None, fill_method = None):
    """Skewness

    Skewness is a measure of the asymmetry of the probability distribution of a real-valued random variable about its mean. 
    The skewness value can be positive or negative, or even undefined.

    source:
    https://www.investopedia.com/terms/s/skewness.asp

    :param data: dataset in DataFrame format
    :param length: period to consider
    :param offset: how many periods to offset the result
    :param fillna: how to handle NaN values
    :param fill_method: NaN filling method
    :return: value of skewness
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.skew(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = skewIndicator(data)
    print(data_indicator)