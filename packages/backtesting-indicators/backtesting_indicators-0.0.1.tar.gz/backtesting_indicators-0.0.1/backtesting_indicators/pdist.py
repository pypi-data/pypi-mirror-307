from backtesting._util import _Data
import pandas_ta as ta



def pdistIndicator(data:_Data, drift:int = 1):
    """
    pdistIndicator(data:_Data, drift:int = 1)
    
    Esta funcion calcula la distancia entre los precios de apertura, cierre, maximo y minimo de un activo.
    
    Parametros:
    data:_Data: Es un objeto de la clase _Data que contiene los precios de apertura, cierre, maximo y minimo de un activo.
    drift:int = 1: Es un entero que indica el numero de periodos hacia atras que se va a calcular la distancia.
    
    Retorna:
    rs: Es una serie de tiempo que contiene la distancia entre los precios de apertura, cierre, maximo y minimo de un activo.
    """
    Open = data.Open
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'open_': Open.s,
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'drift': drift,
    }    
    
    rs = ta.pdist(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pdistIndicator(data)
    print(data_indicator)