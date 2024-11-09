from backtesting._util import _Data
import pandas_ta as ta


def aboveIndicator(data:_Data, length:int = 10):
    """
    aboveIndicator(data:_Data, length:int = 10)
    
    Esta funcion recibe un objeto de tipo _Data y un entero length, y devuelve un objeto de tipo Series.
    
    Esta funcion calcula si el precio de cierre de un activo esta por encima de su media movil exponencial.
    
    Parametros:
    data:_Data: Un objeto de tipo _Data.
    length:int: Un entero que representa el periodo de la media movil exponencial.
    
    Retorno:
    rs: Un objeto de tipo Series.
    """
    Close = data.Close
    EMA = data.EMA
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.above(EMA, Close, **attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = aboveIndicator(data)
    print(data_indicator)