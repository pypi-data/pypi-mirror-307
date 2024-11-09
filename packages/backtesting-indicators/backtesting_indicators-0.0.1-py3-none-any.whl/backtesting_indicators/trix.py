from backtesting._util import _Data
import pandas_ta as ta


def trixIndicator(data:_Data, length:int = 18, signal:int = 9, scalar:float = 100, drift:int = 1, offset:int = 0):
    """
    trixIndicator(data:_Data, length:int = 18, signal:int = 9, scalar:float = 100, drift:int = 1, offset:int = 0)
    
    Trix Indicator
    
    Parametros:
    data: _Data : Data de entrada
    length: int : Periodo de la media movil
    signal: int : Periodo de la seÃ±al
    scalar: float : Escalar
    drift: int : Deriva
    offset: int : Desplazamiento
    
    Retorna:
    rs : pd.Series : Trix Indicator
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'signal': signal,
        'scalar': scalar,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.trix(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = trixIndicator(data)
    print(data_indicator)