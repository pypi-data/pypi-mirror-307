from backtesting._util import _Data
import pandas_ta as ta


def true_rangeIndicator(data:_Data, drift:int = 1, offset:int = 0):
    """
    true_rangeIndicator(data:_Data, drift:int = 1, offset:int = 0)
    
    True Range Indicator
    
    Parametros:
    data: _Data : Dataframe con los datos de OHLC
    drift: int : Valor por defecto 1
    offset: int : Valor por defecto 0
    
    Retorna:
    rs : pd.Series : Serie con el True Range
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.true_range(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = true_rangeIndicator(data)
    print(data_indicator)