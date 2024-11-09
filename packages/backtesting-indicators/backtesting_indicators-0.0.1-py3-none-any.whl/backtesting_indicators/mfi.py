from backtesting._util import _Data
import pandas_ta as ta


def mfiIndicator(data:_Data, length:int = 14, drift:int = 1):
    """
    MFI (Money Flow Index) es un indicador de impulso que utiliza el precio y el volumen para predecir la fiabilidad de la tendencia actual.
    El MFI es un indicador de sobrecompra o sobreventa, que oscila entre 0 y 100.
    Un MFI por encima de 80 se considera sobrecompra y por debajo de 20 se considera sobreventa.
    """
    high = data.High
    low = data.Low
    close = data.Close
    volume = data.Volume
    
    attr = {
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'volume': volume.s,
        'length': length,
        'drift': drift,
    }    
    
    rs = ta.mfi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = mfiIndicator(data)
    print(data_indicator)