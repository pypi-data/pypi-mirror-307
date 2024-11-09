from backtesting._util import _Data
import pandas_ta as ta


def demaIndicator(data:_Data, length:int = 10):
    """
    demaIndicator(data:_Data, length:int = 10)
    
    Funcion que calcula el Double Exponential Moving Average (DEMA) de una serie de precios.
    
    Parametros:
    data: _Data: Serie de precios.
    length: int: Numero de periodos a considerar.
    
    Retorna:
    rs: pd.Series: Serie con el DEMA calculado.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.dema(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = demaIndicator(data)
    print(data_indicator)