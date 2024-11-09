from backtesting._util import _Data
import pandas_ta as ta


def momIndicator(data:_Data, length:int = 1):
    """
    Momentum (MOM)

    Momentum measures the rate of the rise or fall in stock prices. It indicates the strength of the price movement. 
    The formula for momentum is simply the difference between the current price and the price a certain number of periods ago. 
    The default period is 1. 

    :param data: data to use
    :param length: period
    :return: MOM
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.mom(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = momIndicator(data)
    print(data_indicator)