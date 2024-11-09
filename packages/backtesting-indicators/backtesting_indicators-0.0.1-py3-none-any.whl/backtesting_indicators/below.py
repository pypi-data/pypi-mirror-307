from backtesting._util import _Data
import pandas_ta as ta


def belowIndicator(data:_Data, length:int = 10):
    """
    belowIndicator(data:_Data, length:int = 10)
    
    Funcion que devuelve un indicador de si el precio de cierre esta por debajo de la media movil
    
    Parametros:
    data:_Data : Dataframe con los datos de la accion
    length:int : Longitud de la media movil
    
    Retorna:
    rs : Indicador de si el precio de cierre esta por debajo de la media movil
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.below(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = belowIndicator(data)
    print(data_indicator)