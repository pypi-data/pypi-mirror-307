from backtesting._util import _Data
import pandas_ta as ta

def xsignalsIndicator(data:_Data, xa:int, xb:int, above:bool = True, long:bool = True, drift:int = 1, offset:int = 0, asbool:bool = False, trend_reset:int = 0, trade_offset:int = 0, fillna:float = None, fill_method:str = None):
    """
    xsignalsIndicator(data:_Data, xa:int, xb:int, above:bool = True, long:bool = True, drift:int = 1, offset:int = 0, asbool:bool = False, trend_reset:int = 0, trade_offset:int = 0, fillna:float = None, fill_method:str = None)
    
    xsignalsIndicator es una funciÃ³n de la libreria ta que permite obtener seÃ±ales de compra y venta de un activo.
    
    ParÃ¡metros:
    data:_Data: Es el conjunto de datos que se utilizara para obtener las seÃ±ales.
    xa:int: Es el valor de la media movil corta.
    xb:int: Es el valor de la media movil larga.
    above:bool: Es un valor booleano que indica si la seÃ±al de compra se activa cuando la media movil corta esta por encima de la media movil larga.
    long:bool: Es un valor booleano que indica si la seÃ±al de compra se activa cuando la media movil corta esta por debajo de la media movil larga.
    drift:int: Es el valor de drift.
    offset:int: Es el valor de offset.
    asbool:bool: Es un valor booleano que indica si se retorna un valor booleano.
    trend_reset:int: Es el valor de trend_reset.
    trade_offset:int: Es el valor de trade_offset.
    fillna:float: Es el valor de fillna.
    fill_method:str: Es el valor de fill_method.
    
    Retorna:
    rs: Es el valor de retorno de la funciÃ³n.
    """
    attr = {
        'xa': xa,
        'xb': xb,
        'above': above,
        'long': long,
        'drift': drift,
        'offset': offset,
        'asbool': asbool,
        'trend_reset': trend_reset,
        'trade_offset': trade_offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }
    
    rs = ta.xsignals(data.s, **attr)
    
    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = xsignalsIndicator(data, 9, 21)
    print(data_indicator)
