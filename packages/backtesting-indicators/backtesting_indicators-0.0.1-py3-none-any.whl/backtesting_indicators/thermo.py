from backtesting._util import _Data
import pandas_ta as ta


def thermoIndicator(data:_Data, length:int = 20, drift:int = 1, mamode:str = 'ema', long:int = 2, short:float = 0.5):
    """
    Funcion que calcula el indicador termo
    
    data: _Data
    length: int
    drift: int
    mamode: str
    long: int
    short: float
    
    return: rs
    """
    High = data.High
    Low = data.Low
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'long': long,
        'short': short,
        'length': length,
        'mamode': mamode,
        'drift': drift,
    }    
    
    rs = ta.thermo(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = thermoIndicator(data)
    print(data_indicator)