from backtesting._util import _Data
import pandas_ta as ta


def macdIndicator(data:_Data, fast:int = 12, slow:int = 26, signal:int = 9, talib:bool = True, offset:int = 0, asmode:bool = False, fillna:bool = False, fill_method:bool = None):
    """
    macdIndicator(data:_Data, fast:int = 12, slow:int = 26, signal:int = 9, talib:bool = True, offset:int = 0, asmode:bool = False, fillna:bool = False, fill_method:bool = None)
    
    Calcula el Moving Average Convergence Divergence (MACD) usando la libreria TA-Lib.
    
    Args:
    data (_Data): El objeto de datos que contiene los precios.
    fast (int): El periodo de la media rapida. Por defecto es 12.
    slow (int): El periodo de la media lenta. Por defecto es 26.
    signal (int): El periodo de la seÃ±al. Por defecto es 9.
    talib (bool): Si se usa TA-Lib. Por defecto es True.
    offset (int): El desplazamiento de la seÃ±al. Por defecto es 0.
    asmode (bool): Si se usa el modo asincrono. Por defecto es False.
    fillna (bool): Si se rellenan los valores NaN. Por defecto es False.
    fill_method (bool): El metodo de relleno. Por defecto es None.
    
    Returns:
    rs (pd.Series): La serie de datos del MACD.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'fast': fast,
        'slow': slow,
        'signal': signal,
        'talib': talib,
        'offset': offset,
        'asmode': asmode,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.macd(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = macdIndicator(data)
    print(data_indicator)