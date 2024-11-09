from backtesting._util import _Data
import pandas_ta as ta


def kstIndicator(data:_Data, roc1:int = 10, roc2:int = 15, roc3:int = 20, roc4:int = 30, sma1:int = 10, sma2:int = 10, sma3:int = 10, sma4:int = 15, signal:int = 9, drift:int = 1):
    """
    kstIndicator(data:_Data, roc1:int = 10, roc2:int = 15, roc3:int = 20, roc4:int = 30, sma1:int = 10, sma2:int = 10, sma3:int = 10, sma4:int = 15, signal:int = 9, drift:int = 1)
    
    Funcion que recibe un objeto de tipo _Data y devuelve el indicador KST.
    
    Parametros:
    - data: Un objeto de tipo _Data que contiene los datos necesarios para calcular el indicador.
    - roc1: Periodo de la media movil.
    - roc2: Periodo de la media movil.
    - roc3: Periodo de la media movil.
    - roc4: Periodo de la media movil.
    - sma1: Periodo de la media movil.
    - sma2: Periodo de la media movil.
    - sma3: Periodo de la media movil.
    - sma4: Periodo de la media movil.
    - signal: Periodo de la media movil.
    - drift: Periodo de la media movil.
    
    Retorna:
    - Un objeto de tipo _Data con el indicador KST.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'roc1': roc1,
        'roc2': roc2,
        'roc3': roc3,
        'roc4': roc4,
        'sma1': sma1,
        'sma2': sma2,
        'sma3': sma3,
        'sma4': sma4,
        'signal': signal,
        'drift': drift
    }    
    
    rs = ta.kst(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = kstIndicator(data)
    print(data_indicator.data)