from backtesting._util import _Data
import pandas_ta as ta


def cciIndicator(data:_Data, length:int = 14, c:float = 0.015):
    """
    cciIndicator(data:_Data, length:int = 14, c:float = 0.015)
    
    Commodity Channel Index (CCI) es un oscilador de impulso que se utiliza para identificar condiciones de sobrecompra o sobreventa en un activo.
    El indicador se compara con un nivel de sobrecompra y sobreventa, que se establece en 100 y -100, respectivamente.
    
    Args:
    data (_Data): Data Class
    length (int): The number of periods to look back.
    c (float): A constant to multiply the mean deviation by.
    
    Returns:
    pd.Series: New feature generated.
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
        'c': c,
    }    
    
    rs = ta.cci(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cciIndicator(data)
    print(data_indicator)