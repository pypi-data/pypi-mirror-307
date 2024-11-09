from backtesting._util import _Data
import pandas_ta as ta


def hl2Indicator(data:_Data):
    """
    hl2Indicator(data:_Data)
    
    Funcion que calcula el indicador hl2
    
    Parametros:
    data: _Data - Dataframe con los datos de entrada
    
    Retorna:
    rs: pd.Series - Serie con los datos calculados
    """
    High = data.High
    Low = data.Low
    
    attr = {
        'high': High.s,
        'low': Low.s,
    }    
    
    rs = ta.hl2(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = hl2Indicator(data)
    print(data_indicator)