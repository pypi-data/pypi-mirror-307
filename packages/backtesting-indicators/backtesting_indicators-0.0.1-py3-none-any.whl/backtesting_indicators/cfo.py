from backtesting._util import _Data
import pandas_ta as ta


def cfoIndicator(data:_Data, length:int = 9, scalar:float = 100, drift:int = 1, offset:int = 0):
    """
    cfoIndicator(data:_Data, length:int = 9, scalar:float = 100, drift:int = 1, offset:int = 0)
    
    Chaikin Oscillator (CFO)
    
    ParÃ¡metros:
    data: _Data - Data de entrada
    length: int - Periodo de la media
    scalar: float - Escalar
    drift: int - Deriva
    offset: int - Desplazamiento
    
    Retorna:
    _Data - Data con el Chaikin Oscillator
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'scalar': scalar,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.cfo(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cfoIndicator(data)
    print(data_indicator)