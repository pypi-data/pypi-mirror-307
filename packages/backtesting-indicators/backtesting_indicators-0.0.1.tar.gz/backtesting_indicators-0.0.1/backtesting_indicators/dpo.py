from backtesting._util import _Data
import pandas_ta as ta


def dpoIndicator(data:_Data, length:int = 20, centered:bool = True, offset:int = 0):
    """
    dpoIndicator(data:_Data, length:int = 20, centered:bool = True, offset:int = 0)
    
    Devuelve el Oscilador de Precios Desplazados (DPO) de una serie de precios.
    
    Parametros:
    - data: Serie de precios.
    - length: Numero de periodos a considerar.
    - centered: Si es True, el DPO se centrara en la mitad del periodo.
    - offset: Desplazamiento de la serie.
    
    Retornos:
    - Serie de precios.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'centered': centered,
        'offset': offset,
    }    
    
    rs = ta.dpo(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = dpoIndicator(data)
    print(data_indicator)