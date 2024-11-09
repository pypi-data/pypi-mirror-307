from backtesting._util import _Data
import pandas_ta as ta


def kvoIndicator(data:_Data, fast:int = 34, slow:int = 55, signal:int = 13, drift:int = 1):
    """
    kvoIndicator(data:_Data, fast:int = 34, slow:int = 55, signal:int = 13, drift:int = 1)
    
    Klinger Volume Oscillator (KVO)
    
    ParÃ¡metros:
    data: _Data - Dataframe con los datos de OHLCV
    fast: int - NÃºmero de periodos para la media rÃ¡pida
    slow: int - NÃºmero de periodos para la media lenta
    signal: int - NÃºmero de periodos para la seÃ±al
    drift: int - NÃºmero de periodos para el drift
    
    Retorna:
    rs: pd.Series - Serie de tiempo con el indicador KVO
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'volume': Volume.s,
        'fast': fast,
        'long': slow,
        'length_sig': signal,
        'mamode': 'ema',
        'offset': 0,
    }    
    
    rs = ta.kvo(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = kvoIndicator(data)
    print(data_indicator)
