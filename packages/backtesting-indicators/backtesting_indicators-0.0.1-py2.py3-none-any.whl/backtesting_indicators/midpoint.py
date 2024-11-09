from backtesting._util import _Data
import pandas_ta as ta


def midpointIndicator(data:_Data, length:int = 10):
    """
    Midpoint - Function

    Inputs:
    data: Data
    length: int = 10

    Outputs:
    rs: pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.midpoint(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = midpointIndicator(data)
    print(data_indicator)