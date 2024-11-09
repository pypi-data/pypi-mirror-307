from backtesting._util import _Data
import pandas_ta as ta


def adIndicator(data:_Data, open:pd.Series, high:pd.Series, low:pd.Series, volume:pd.Series, talib:bool = True, offset:int = 0, fillna:float = None, fill_method:str = None):
    """
    adIndicator - Accumulation/Distribution (AD) Indicator

    Inputs:
    data: _Data
    open: pd.Series
    high: pd.Series
    low: pd.Series
    volume: pd.Series
    talib: bool = True
    offset: int = 0
    fillna: float = None
    fill_method: str = None

    Output:
    pd.Series
    """
    attr = {
        'high': high,
        'low': low,
        'close': data.Close.s,
        'volume': volume,
        'open': open,
        'talib': talib,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }
    
    rs = ta.ad(**attr)
    
    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = adIndicator(data, data.Open, data.High, data.Low, data.Volume)
    print(data_indicator)