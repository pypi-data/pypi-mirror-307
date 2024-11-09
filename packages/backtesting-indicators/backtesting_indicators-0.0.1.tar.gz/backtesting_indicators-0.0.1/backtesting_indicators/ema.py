from backtesting._util import _Data
import pandas_ta as ta


def emaIndicator(data:_Data, length:int = 10):
    """
    emaIndicator(data:_Data, length:int = 10)
    
    Calcula el Exponential Moving Average de una serie de tiempo.
    
    Parametros:
    data : _Data : Dataframe con los datos de la serie de tiempo.
    length : int : Numero de periodos a considerar para el calculo.
    
    Retorna:
    pd.Series : Serie de tiempo con el Exponential Moving Average.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.ema(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = emaIndicator(data)
    print(data_indicator)