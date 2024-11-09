from backtesting._util import _Data
import pandas_ta as ta


def cmoIndicator(data:_Data, scalar:float = 100, drift:int = 1, offset:int = 0, talib:bool = True, fillna:bool = False, fill_method:str = 'pad'):
    """
    cmoIndicator(data:_Data, scalar:float = 100, drift:int = 1, offset:int = 0, talib:bool = True, fillna:bool = False, fill_method:str = 'pad')
    
    Commodity Channel Index (CCI)
    
    ParÃ¡metros:
    data: pd.DataFrame - DataFrame con los precios de cierre.
    scalar: float - Escalar para el indicador.
    drift: int - Drift o desplazamiento.
    offset: int - Offset o sesgo.
    talib: bool - Usar la librerÃ­a TA-Lib.
    fillna: bool - Determinar si se llenarÃ¡n los valores faltantes.
    fill_method: str - MÃ©todo de llenado de valores faltantes.
    
    Retorna:
    pd.Series - Indicador CCI.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'scalar': scalar,
        'drift': drift,
        'offset': offset,
        'talib': talib,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.cmo(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cmoIndicator(data)
    print(data_indicator)