from backtesting._util import _Data
import pandas_ta as ta


def sinwmaIndicator(data:_Data, length:int = 10):
    """
    sinwmaIndicator(data:_Data, length:int = 10)
    
    Funcion que calcula el indicador sinwma.
    
    Parametros:
    data: _Data: Dataframe con los datos de entrada.
    length: int: Numero de periodos a considerar.
    
    Retorna:
    rs: pd.Series: Serie con el resultado del indicador.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.sinwma(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = sinwmaIndicator(data)
    print(data_indicator)