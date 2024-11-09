from backtesting._util import _Data
import pandas_ta as ta

def supertrendIndicator(data:_Data, length:int = 7, multiplier:float = 3.0, offset:int = 0):
    """
    Funcion que calcula el indicador de supertrend
    
    Parametros:
    data : _Data : Dataframe con los datos de High, Low y Close
    length : int : Numero de periodos para el calculo
    multiplier : float : Multiplicador para el calculo
    offset : int : Offset para el calculo
    
    Retorno:
    pd.Series : Serie con los valores del indicador
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
        'multiplier': multiplier,
        'offset': offset,
    }    
    
    rs = ta.supertrend(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = supertrendIndicator(data)
    print(data_indicator)

