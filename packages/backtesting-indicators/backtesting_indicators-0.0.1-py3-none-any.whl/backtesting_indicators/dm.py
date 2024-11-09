from backtesting._util import _Data
import pandas_ta as ta


def dmIndicator(data:_Data, length:int = 14, mamode:str = "rma", drift:int = 1, talib:bool = True, offset:int = 0):
    """
    dmIndicator(data:_Data, length:int = 14, mamode:str = "rma", drift:int = 1, talib:bool = True, offset:int = 0)
    
    Directional Movement Indicator (DMI)
    
    Inputs:
      data:  _Data
      length: int = 14
      mamode: str = "rma"
      drift: int = 1
      talib: bool = True
      offset: int = 0
    """
    high = data.High
    low = data.Low
    
    attr = {
        'high': high.s,
        'low': low.s,
        'mamode': mamode,
        'drift': drift,
        'talib': talib,
        'offset': offset,
    }    
    
    rs = ta.dm(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = dmIndicator(data)
    print(data_indicator)
