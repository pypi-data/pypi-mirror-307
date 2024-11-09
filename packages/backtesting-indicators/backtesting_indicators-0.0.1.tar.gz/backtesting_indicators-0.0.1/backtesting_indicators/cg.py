from backtesting._util import _Data
import pandas_ta as ta


def cgIndicator(data:_Data, length:int = 10, offset:int = 0):
    """
    cgIndicator(data:_Data, length:int = 10, offset:int = 0)
    
    Funcion que calcula el indicador cg
    
    Parametros:
    data : _Data : Dataframe con los datos de entrada
    length : int : Longitud de la serie
    offset : int : Desplazamiento
    
    Retorna:
    rs : pd.Series : Serie con el indicador calculado
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'offset': offset,
    }    
    
    rs = ta.cg(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cgIndicator(data)
    print(data_indicator)