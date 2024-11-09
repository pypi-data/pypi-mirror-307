from backtesting._util import _Data
import pandas_ta as ta


def long_runIndicator(data:_Data, length:int = 10):
    """
    long_runIndicator(data:_Data, length:int = 10)
    
    long_runIndicator es un indicador de tendencia que se calcula a partir de la media movil de los precios de cierre.
    
    Parametros:
    data:_Data: Es el objeto de datos que contiene los precios de cierre.
    length:int: Es el numero de periodos que se usara para calcular la media movil.
    
    Retornos:
    pd.Series: Es una serie de pandas que contiene los valores del indicador.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.long_run(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = long_runIndicator(data)
    print(data_indicator)