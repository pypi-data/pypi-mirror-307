from backtesting._util import _Data
import pandas_ta as ta


def hlc3Indicator(data:_Data):
    """
    hlc3Indicator(data:_Data)
    
    Funcion que calcula el indicador hlc3
    
    Parametros:
    data:_Data: Dataframe con los datos de High, Low y Close
    
    Return:
    rs: Serie con el indicador hlc3
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
    }    
    
    rs = ta.hlc3(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = hlc3Indicator(data)
    print(data_indicator)