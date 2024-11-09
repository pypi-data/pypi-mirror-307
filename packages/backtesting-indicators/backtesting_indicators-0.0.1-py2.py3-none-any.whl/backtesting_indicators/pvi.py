from backtesting._util import _Data
import pandas_ta as ta


def pviIndicator(data:_Data, length:int = 13, initial:int = 1000, offset:int = 0):
    """
    pviIndicator(data:_Data, length:int = 13, initial:int = 1000, offset:int = 0)
    
    PVI (Positive Volume Index) es un indicador que mide la fuerza de una tendencia alcista. 
    Se calcula sumando el porcentaje de cambio del precio de cierre de un periodo al PVI del periodo anterior 
    si el volumen de negociaciÃ³n es mayor que el periodo anterior. 
    Si el volumen de negociaciÃ³n es menor que el periodo anterior, el PVI se mantiene igual que el periodo anterior.
    
    Args:
        data (_Data): Data Class
        length (int, optional): Longitud de la serie. Defaults to 13.
        initial (int, optional): Valor inicial. Defaults to 1000.
        offset (int, optional): Desplazamiento. Defaults to 0.
    
    Returns:
        pd.Series: Resultado
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
    
    rs = ta.pvi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pviIndicator(data)
    print(data_indicator)