from backtesting._util import _Data
import pandas_ta as ta


def stochIndicator(data:_Data, k:int = 14, d:int = 3, smooth_k:int = 3, mamode:str = 'sma', offset:int = 0):
    """
    stochIndicator(data:_Data, k:int = 14, d:int = 3, smooth_k:int = 3, mamode:str = 'sma', offset:int = 0)
    
    Calcula el indicador estocÃ¡stico
    
    Parametros:
    data : _Data : Dataframe con los datos de entrada
    k : int : Periodo para el calculo de %K
    d : int : Periodo para el calculo de %D
    smooth_k : int : Periodo para el suavizado de %K
    mamode : str : Modo de la media movil
    offset : int : Desplazamiento de la serie
    
    Retorna:
    pd.Series : Serie con los valores del indicador
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'k': k,
        'd': d,
        'smooth_k': smooth_k,
        'mamode': mamode,
        'offset': offset,
    }    
    
    rs = ta.stoch(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = stochIndicator(data)
    print(data_indicator)
