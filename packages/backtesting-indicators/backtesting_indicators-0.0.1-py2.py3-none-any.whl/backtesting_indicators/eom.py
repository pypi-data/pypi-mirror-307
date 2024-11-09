from backtesting._util import _Data
import pandas_ta as ta


def eomIndicator(data:_Data, length:int = 14, divisor:int = 100000000, drift:int = 1):
    """
    Esta funcion calcula el indicador EOM (Ease of Movement) para un conjunto de datos.
    
    Parametros:
    data : _Data : Un objeto de tipo _Data que contiene los datos necesarios para el calculo del indicador.
    length : int : El periodo de tiempo que se utilizara para el calculo del indicador.
    divisor : int : El divisor que se utilizara para el calculo del indicador.
    drift : int : El drift que se utilizara para el calculo del indicador.
    
    Retorna:
    _Data : Un objeto de tipo _Data que contiene el indicador calculado.
    """
    high = data.High
    low = data.Low
    close = data.Close
    volume = data.Volume
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'volume': volume.s,
        'length': length,
        'divisor': divisor,
        'drift': drift
    }
    
    rs = ta.eom(**attr)
    
    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = eomIndicator(data)
    print(data_indicator)