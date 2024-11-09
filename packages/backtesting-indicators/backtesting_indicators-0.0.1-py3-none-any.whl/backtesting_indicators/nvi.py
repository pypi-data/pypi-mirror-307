from backtesting._util import _Data
import pandas_ta as ta


def nviIndicator(data:_Data, length:int = 1, initial:int = 1000, offset:int = 0):
    """
    nviIndicator(data:_Data, length:int = 1, initial:int = 1000, offset:int = 0)
    
    Funcion que calcula el indicador de Net Volume Indicator (NVI)
    
    Parametros:
    data : _Data : Dataframe con los datos de entrada
    length : int : Numero de periodos
    initial : int : Valor inicial
    offset : int : Desplazamiento
    
    Retorna:
    rs : pd.Series : Serie con el resultado del indicador
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
        'length': length,
        'initial': initial,
        'offset': offset,
    }    
    
    rs = ta.nvi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = nviIndicator(data)
    print(data_indicator)