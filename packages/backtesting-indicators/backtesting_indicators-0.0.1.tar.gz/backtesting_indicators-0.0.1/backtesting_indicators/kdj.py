from backtesting._util import _Data
import pandas_ta as ta


def kdjIndicator(data:_Data, length:int = 9, signal:int = 3):
    """
    kdjIndicator(data:_Data, length:int = 9, signal:int = 3)
    
    Funcion que calcula el indicador KDJ
    
    Parametros:
    data:_Data: Dataframe con los datos de High, Low y Close
    length:int: Periodo para calcular el KDJ
    signal:int: Periodo para calcular la senal
    
    Retorna:
    Dataframe con los valores de KDJ y senal
    """
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'signal': signal,
    }    
    
    rs = ta.kdj(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = kdjIndicator(data)
    print(data_indicator)