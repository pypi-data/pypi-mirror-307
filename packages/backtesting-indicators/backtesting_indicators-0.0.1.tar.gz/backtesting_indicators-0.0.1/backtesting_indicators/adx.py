from backtesting._util import _Data
import pandas_ta as ta


def adxIndicator(data:_Data, length:int = 14, lensig:int = 14, scalar:float = 100, mamode:str = 'rma', drift:int = 1, offset:int = 0):
    """
    adxIndicator(data:_Data, length:int = 14, lensig:int = 14, scalar:float = 100, mamode:str = 'rma', drift:int = 1, offset:int = 0)
    
    ADX - Average Directional Movement Index
    
    Inputs:
      data: _Data
      length: int = 14
      lensig: int = 14
      scalar: float = 100
      mamode: str = 'rma'
      drift: int = 1
      offset: int = 0
      
    Outputs:
      rs: _Data
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'lensig': lensig,
        'scalar': scalar,
        'mamode': mamode,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.adx(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = adxIndicator(data)
    print(data_indicator)