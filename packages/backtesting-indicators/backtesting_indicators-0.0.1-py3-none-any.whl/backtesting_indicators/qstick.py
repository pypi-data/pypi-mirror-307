from backtesting._util import _Data
import pandas_ta as ta


def qstickIndicator(data:_Data, length:int = 10, ma:str = None, offset:int = 0):
    """
    qstickIndicator(data:_Data, length:int = 10, ma:str = None, offset:int = 0)
    
    Qstick Indicator
    
    ParÃ¡metros:
    data: _Data : Dataframe con los datos de OHLC
    length: int : Periodo de la media movil
    ma: str : Tipo de media movil
    offset: int : Desplazamiento de la media movil
    
    Retorna:
    rs : pd.Series : Serie con el resultado del indicador
    """
    Open = data.Open
    Close = data.Close
    
    attr = {
        'open': Open.s,
        'close': Close.s,
        'length': length,
        'ma': ma,
        'offset': offset,
    }    
    
    rs = ta.qstick(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = qstickIndicator(data)
    print(data_indicator)