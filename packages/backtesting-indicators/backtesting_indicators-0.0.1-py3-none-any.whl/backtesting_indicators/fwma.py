from backtesting._util import _Data
import pandas_ta as ta


def fwmaIndicator(data:_Data, length:int = 10, asc:bool = True, offset:int = 0, fillna = None, fill_method = None):
    """
    fwmaIndicator(data:_Data, length:int = 10, asc:bool = True, offset:int = 0, fillna = None, fill_method = None)
    
    Funcion que calcula el indicador de Moving Average Weighted Average (FWMA)
    
    Parametros:
    data: pd.DataFrame - Dataframe de datos
    length: int - Numero de periodos
    asc: bool - Orden de los periodos
    offset: int - Desplazamiento de los periodos
    fillna: None - Valor de relleno
    fill_method: None - Metodo de relleno
    
    Retorna:
    pd.Series - Serie de datos calculados
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'asc': asc,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method
    }    
    
    rs = ta.fwma(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = fwmaIndicator(data)
    print(data_indicator)