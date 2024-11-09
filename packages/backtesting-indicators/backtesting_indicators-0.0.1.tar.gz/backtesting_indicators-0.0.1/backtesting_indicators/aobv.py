from backtesting._util import _Data
import pandas_ta as ta

def aobvIndicator(data:_Data, length:int = 10):
    """
    aobvIndicator(data:_Data, length:int = 10)
    
    Accumulation / Distribution (A/D) Oscillator
    
    params:
    - data: _Data
    - length: int = 10
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
        'length': length,
    }    
    
    rs = ta.aobv(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = aobvIndicator(data)
    print(data_indicator)
