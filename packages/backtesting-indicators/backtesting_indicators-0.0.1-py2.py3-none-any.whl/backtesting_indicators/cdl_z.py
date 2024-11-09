from backtesting._util import _Data
import pandas_ta as ta


def cdl_zIndicator(data:_Data, length:int = 10):
    """
    cdl_zIndicator(data:_Data, length:int = 10)
    
    Funcion que calcula el cdl_zIndicator
    
    Parametros:
    data:_Data: Dataframe con los datos de OHLC
    length:int: Longitud de la serie
    
    Return:
    rs: Serie con el cdl_zIndicator
    """
    open_ = data.Open
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'open_': open_.s,
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
    }    
    
    rs = ta.cdl_z(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cdl_zIndicator(data)
    print(data_indicator)