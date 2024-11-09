from backtesting._util import _Data
import pandas_ta as ta


def hiloIndicator(data:_Data, high_length:int = 13, low_length:int = 21, mamode:str = "sma", offset:int = 0, adjust:bool = True, presma:bool = False, fillna:bool = False, fill_method:bool = False):
    """
    hiloIndicator(data:_Data, high_length:int = 13, low_length:int = 21, mamode:str = "sma", offset:int = 0, adjust:bool = True, presma:bool = False, fillna:bool = False, fill_method:bool = False)
    
    Hilo Indicator
    
    ParÃ¡metros:
    data: _Data - Dataframe
    high_length: int - High Length
    low_length: int - Low Length
    mamode: str - MA Mode
    offset: int - Offset
    adjust: bool - Adjust
    presma: bool - Presma
    fillna: bool - Fillna
    fill_method: bool - Fill Method
    
    Retorna:
    rs - Resultado
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'high_length': high_length,
        'low_length': low_length,
        'mamode': mamode,
        'offset': offset,
        'adjust': adjust,
        'presma': presma,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.hilo(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = hiloIndicator(data)
    print(data_indicator)