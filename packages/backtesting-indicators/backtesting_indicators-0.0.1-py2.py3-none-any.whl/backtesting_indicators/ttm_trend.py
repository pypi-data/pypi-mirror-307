from backtesting._util import _Data
import pandas_ta as ta


def ttm_trendIndicator(data:_Data, length:int = 6, offset:int = 0):
    """
    ttm_trendIndicator(data:_Data, length:int = 6, offset:int = 0)
    
    TTM Trend Indicator
    
    Parametros:
    data : _Data : Data
    length : int : Length
    offset : int : Offset
    
    Retorna:
    _Data : Data
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'offset': offset,
    }    
    
    rs = ta.ttm_trend(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ttm_trendIndicator(data)
    print(data_indicator)