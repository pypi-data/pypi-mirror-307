from backtesting._util import _Data
import pandas_ta as ta


def pwmaIndicator(data:_Data, length:int = 10, asc:bool = True, offset:int = 0):
    """
    pwmaIndicator(data:_Data, length:int = 10, asc:bool = True, offset:int = 0)
    
    Promedio ponderado de la media movil
    
    Parametros:
    data: _Data
    length: int
    asc: bool
    offset: int
    
    Retorna:
    rs
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'asc': asc,
        'offset': offset,
    }    
    
    rs = ta.pwma(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pwmaIndicator(data)
    print(data_indicator)