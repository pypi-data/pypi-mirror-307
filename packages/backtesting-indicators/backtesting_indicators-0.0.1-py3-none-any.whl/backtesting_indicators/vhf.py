from backtesting._util import _Data
import pandas_ta as ta


def vhfIndicator(data:_Data, length:int = 28):
    """
    VHF (Vertical Horizontal Filter) es un indicador que identifica si el mercado esta en una tendencia o en un rango.
    Si el valor es menor a 1, el mercado esta en un rango, si es mayor a 1, el mercado esta en una tendencia.
    """
    Close = data.Close
    
    attr = {
        'source': Close.s,
        'length': length,
    }    
    
    rs = ta.vhf(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = vhfIndicator(data)
    print(data_indicator)