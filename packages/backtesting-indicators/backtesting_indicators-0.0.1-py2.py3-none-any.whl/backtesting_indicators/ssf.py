from backtesting._util import _Data
import pandas_ta as ta


def ssfIndicator(data:_Data, length:int = 10, poles:int = 2):
    """
    ssfIndicator(data:_Data, length:int = 10, poles:int = 2)
    
    ssfIndicator es un indicador de tendencia que se basa en la transformada de Fourier
    para calcular la tendencia de un activo.
    
    Args:
    data (_Data): El conjunto de datos sobre el que se calculara el indicador.
    length (int): El periodo de tiempo que se utilizara para calcular el indicador.
    poles (int): El numero de polos que se utilizara para calcular el indicador.
    
    Returns:
    _Data: Un objeto de tipo _Data con el indicador calculado.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'poles': poles,
    }    
    
    rs = ta.ssf(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ssfIndicator(data)
    print(data_indicator.data)