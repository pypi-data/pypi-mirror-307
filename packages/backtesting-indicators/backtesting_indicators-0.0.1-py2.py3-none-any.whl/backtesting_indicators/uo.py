from backtesting._util import _Data
import pandas_ta as ta


def uoIndicator(data:_Data, fast:int = 7, medium:int = 14, slow:int = 28, fast_w:float = 4.0, medium_w:float = 2.0, slow_w:float = 1.0, drift:int = 1):
    """
    uoIndicator(data:_Data, fast:int = 7, medium:int = 14, slow:int = 28, fast_w:float = 4.0, medium_w:float = 2.0, slow_w:float = 1.0, drift:int = 1)
    
    Ultimo Oscilador
    
    Parametros:
    data: _Data : Dataframe con los datos de OHLC
    fast: int : Periodo rapido
    medium: int : Periodo medio
    slow: int : Periodo lento
    fast_w: float : Peso del periodo rapido
    medium_w: float : Peso del periodo medio
    slow_w: float : Peso del periodo lento
    drift: int : Deriva
    
    Retorna:
    pd.Series : Ultimo Oscilador
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'fast': fast,
        'medium': medium,
        'slow': slow,
        'fast_w': fast_w,
        'medium_w': medium_w,
        'slow_w': slow_w,
        'drift': drift,
    }    
    
    rs = ta.uo(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = uoIndicator(data)
    print(data_indicator)