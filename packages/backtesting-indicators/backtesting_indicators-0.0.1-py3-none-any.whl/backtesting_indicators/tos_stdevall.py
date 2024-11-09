from backtesting._util import _Data
import pandas_ta as ta


def tos_stdevallIndicator(data:_Data, length:int = None, stds:list = [1,2,3], ddof:int = 1, offset:int = 0):
    """
    tos_stdevallIndicator(data:_Data, length:int = None, stds:list = [1,2,3], ddof:int = 1, offset:int = 0)
    
    Descripcion:
    Esta funcion calcula la desviacion estandar de una serie de precios
    
    Parametros:
    data: _Data : Dataframe de datos
    length: int : Numero de periodos a considerar
    stds: list : Lista de desviaciones estandar a calcular
    ddof: int : Grados de libertad
    offset: int : Periodos a desplazar
    
    Retornos:
    rs : pd.Series : Serie de datos con la desviacion estandar
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'stds': stds,
        'ddof': ddof,
        'offset': offset,
    }    
    
    rs = ta.tos_stdevall(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = tos_stdevallIndicator(data)
    print(data_indicator)