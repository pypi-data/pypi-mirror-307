from backtesting._util import _Data
import pandas_ta as ta


def jmaIndicator(data:_Data, length:int = 7, phase:float = 0, offset:int = 0):
    """
    jmaIndicator(data:_Data, length:int = 7, phase:float = 0, offset:int = 0)
    
    JMA (Jurik Moving Average) es una media mÃ³vil avanzada que se adapta a la volatilidad del mercado.
    
    ParÃ¡metros:
    data: _Data: Dataframe con los precios de cierre.
    length: int: NÃºmero de periodos para el cÃ¡lculo de la media mÃ³vil.
    phase: float: Fase de la onda sinusoidal.
    offset: int: Desplazamiento de la media mÃ³vil.
    
    Retornos:
    rs: pd.Series: Serie de tiempo con el resultado del indicador.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'phase': phase,
        'offset': offset,
    }    
    
    rs = ta.jma(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = jmaIndicator(data)
    print(data_indicator)