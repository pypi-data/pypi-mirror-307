from backtesting._util import _Data
import pandas_ta as ta


def psarIndicator(data:_Data, af0:float = 0.02, af:float = 0.02, max_af:float = 0.2, offset:int = 0):
    """
    data: _Data
    af0: float = 0.02
    af: float = 0.02
    max_af: float = 0.2
    offset: int = 0
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'af0': af0,
        'af': af,
        'max_af': max_af,
        'offset': offset,
    }    
    
    rs = ta.psar(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = psarIndicator(data)
    print(data_indicator)