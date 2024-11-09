from backtesting._util import _Data
import pandas_ta as ta


def medianIndicator(data:_Data, length:int = 30, offset:int = 0, fillna = None, fill_method = None):
    """
    medianIndicator(data:_Data, length:int = 30, offset:int = 0, fillna = None, fill_method = None)
    
    Media movil de la serie de tiempo.
    
    Parametros:
    data: _Data : Dataframe con los datos de entrada
    length: int : Numero de periodos
    offset: int : Desplazamiento de la media movil
    fillna: None : Rellenar valores NaN
    fill_method: None : Metodo de relleno
    
    Retorna:
    rs : pd.Series : Serie de tiempo con la media movil
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.median(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = medianIndicator(data)
    print(data_indicator)