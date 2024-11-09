from backtesting._util import _Data
import pandas_ta as ta


def obvIndicator(data:_Data):
    """
    obvIndicator(data:_Data)
    
    Funcion que calcula el indicador OBV (On Balance Volume)
    
    Parametros:
    data : _Data : Dataframe con los datos de la serie
    
    Retorna:
    rs : pd.Series : Serie con los valores del indicador
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
    }    
    
    rs = ta.obv(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = obvIndicator(data)
    print(data_indicator)