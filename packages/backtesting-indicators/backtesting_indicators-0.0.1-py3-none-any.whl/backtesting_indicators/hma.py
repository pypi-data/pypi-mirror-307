from backtesting._util import _Data
import pandas_ta as ta


def hmaIndicator(data:_Data, length:int = 10):
    """
    hmaIndicator(data:_Data, length:int = 10)
    
    Funcion que calcula el Hull Moving Average de una serie de precios.
    
    Parametros:
    - data: Serie de precios.
    - length: Numero de periodos a considerar.
    
    Retornos:
    - Serie de precios del Hull Moving Average.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.hma(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = hmaIndicator(data)
    print(data_indicator)