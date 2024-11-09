from backtesting._util import _Data
import pandas_ta as ta


def apoIndicator(data:_Data, fast:int = 12, slow:int = 26, mamode:str = 'sma', talib:bool = True, offset:int = 0):
    """
    apoIndicator(data:_Data, fast:int = 12, slow:int = 26, mamode:str = 'sma', talib:bool = True, offset:int = 0)
    
    ApoIndicator es un indicador de analisis tecnico que se utiliza para determinar la tendencia de un activo financiero.
    
    Parametros:
    data: _Data: Es un objeto de la clase _Data que contiene los datos de un activo financiero.
    fast: int: Es el periodo de tiempo rapido.
    slow: int: Es el periodo de tiempo lento.
    mamode: str: Es el tipo de media movil que se utilizara para calcular el indicador.
    talib: bool: Es un booleano que indica si se utilizara la libreria TA-Lib para calcular el indicador.
    offset: int: Es el desplazamiento del indicador.
    
    Retorna:
    rs: pd.Series: Es una serie de pandas que contiene los valores del indicador.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'fast': fast,
        'slow': slow,
        'mamode': mamode,
        'talib': talib,
        'offset': offset,
    }    
    
    rs = ta.apo(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = apoIndicator(data)
    print(data_indicator)
