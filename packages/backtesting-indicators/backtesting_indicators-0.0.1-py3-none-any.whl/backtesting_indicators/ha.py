from backtesting._util import _Data
import pandas_ta as ta


def haIndicator(data:_Data):
    """
    haIndicator(data:_Data)
    
    Funcion que calcula el indicador Heikin Ashi.
    
    Parametros:
    data: _Data - Data que contiene los precios de Open, High, Low y Close.
    
    Return:
    _Data - Data que contiene los precios de Open, High, Low y Close del indicador Heikin Ashi.
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
    }    
    
    rs = ta.ha(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = haIndicator(data)
    print(data_indicator.df)