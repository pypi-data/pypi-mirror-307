from backtesting._util import _Data
import pandas_ta as ta


def efiIndicator(data:_Data, length:int = 20, drift:int = 1, mamode:str = None):
    """
    efiIndicator(data:_Data, length:int = 20, drift:int = 1, mamode:str = None)
    
    Ease of Movement (EoM, EMV)
    
    Inputs:
      data: _Data
      length: int = 20
      drift: int = 1
      mamode: str = None
    Outputs:
      Series
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
        'length': length,
        'drift': drift,
        'mamode': mamode,
    }    
    
    rs = ta.efi(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = efiIndicator(data)
    print(data_indicator)
