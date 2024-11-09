from backtesting._util import _Data
import pandas_ta as ta


def above_valueIndicator(data:_Data, value:int = 0):
    '''
    above_valueIndicator(data:_Data, value:int = 0)
    
    Funcion que devuelve un indicador de si el precio de cierre esta por encima de un valor dado.
    
    Parametros:
    data : _Data : Dataframe con los datos de la serie de tiempo.
    value : int : Valor de referencia.
    
    Retorno:
    rs : pd.Series : Serie de tiempo con valores booleanos.
    '''
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'value': value,
    }    
    
    rs = ta.above_value(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = above_valueIndicator(data)
    print(data_indicator)