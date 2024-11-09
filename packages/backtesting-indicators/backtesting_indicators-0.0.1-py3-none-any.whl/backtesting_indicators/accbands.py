from backtesting._util import _Data
import pandas_ta as ta


def accbandsIndicator(data:_Data, length:int = 10, c:int = 4, mamode:str = 'sma', drift:int = 1, offset:int = 0):
    """
    accbandsIndicator(data:_Data, length:int = 10, c:int = 4, mamode:str = 'sma', drift:int = 1, offset:int = 0)
    
    AccBands Indicator
    
    ParÃ¡metros:
    data: _Data: Data
    length: int: Number of periods for moving average
    c: int: Number of standard deviations
    mamode: str: Moving average mode
    drift: int: Number of periods to drift the bands
    offset: int: Number of periods to offset the bands
    
    Retorna:
    _Data: Data
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
        'c': c,
        'mamode': mamode,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.accbands(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = accbandsIndicator(data)
    print(data_indicator)