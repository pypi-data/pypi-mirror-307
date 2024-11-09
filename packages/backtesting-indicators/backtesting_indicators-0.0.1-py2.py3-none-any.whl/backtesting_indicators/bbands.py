from backtesting._util import _Data
import pandas_ta as ta


def bbandsIndicator(data:_Data, length:int = 5, std:int = 2, mamode:str = "sma", ddof:int = 0, talib:bool = True, offset:int = 0):
    """
    data: Data
    length: int
    std: int
    mamode: str
    ddof: int
    talib: bool
    offset: int
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'std': std,
        'mamode': mamode,
        'ddof': ddof,
        'talib': talib,
        'offset': offset,
    }    
    
    rs = ta.bbands(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = bbandsIndicator(data)
    print(data_indicator)
    print(data_indicator.columns)