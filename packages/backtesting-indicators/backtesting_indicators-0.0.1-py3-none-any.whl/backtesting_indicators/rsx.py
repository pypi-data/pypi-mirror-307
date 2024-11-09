from backtesting._util import _Data
import pandas_ta as ta


def rsxIndicator(data:_Data, length:int = 14, drift:int = 1, offset:int = 0):
    """
    Funcion que calcula el indicador RSX
    
    Parametros:
    data : _Data : Dataframe con los datos
    length : int : Longitud de la media movil
    drift : int : Deriva
    offset : int : Offset
    
    Retorna:
    rs : pd.Series : Serie con el indicador RSX
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.rsx(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = rsxIndicator(data)
    print(data_indicator)