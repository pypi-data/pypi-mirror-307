from backtesting._util import _Data
import pandas_ta as ta


def smiIndicator(data:_Data, fast:int = 5, slow:int = 20, signal:int = 5, scalar:float = 1, offset:int = 0):
    """
    smiIndicator(data:_Data, fast:int = 5, slow:int = 20, signal:int = 5, scalar:float = 1, offset:int = 0)
    
    SMI (Stochastic Momentum Index)
    
    ParÃ¡metros:
    data: _Data - Dataframe con los datos de entrada
    fast: int - NÃºmero de periodos para la media rÃ¡pida
    slow: int - NÃºmero de periodos para la media lenta
    signal: int - NÃºmero de periodos para la seÃ±al
    scalar: float - Escalar
    offset: int - Desplazamiento
    
    Retorna:
    pd.Series - SMI
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'fast': fast,
        'slow': slow,
        'signal': signal,
        'scalar': scalar,
        'offset': offset,
    }    
    
    rs = ta.smi(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = smiIndicator(data)
    print(data_indicator)
