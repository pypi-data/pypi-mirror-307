from backtesting._util import _Data
import pandas_ta as ta


def inertiaIndicator(data:_Data, length:int = 20, rvi_length:int = 14, refined:bool = False, thirds:bool = False, mamode:str = 'ema', drift:int = 1, offset:int = 0):
    """
    inertiaIndicator(data:_Data, length:int = 20, rvi_length:int = 14, refined:bool = False, thirds:bool = False, mamode:str = 'ema', drift:int = 1, offset:int = 0)
    
    Inertia Indicator
    
    ParÃ¡metros:
    data : _Data : 
        Data
    length : int : 20
        Length
    rvi_length : int : 14
        RVI Length
    refined : bool : False
        Refined
    thirds : bool : False
        Thirds
    mamode : str : 'ema'
        MA Mode
    drift : int : 1
        Drift
    offset : int : 0
        Offset
    
    Retorna:
    rs : _Series : 
        Inertia Indicator
    """
    Open = data.Open
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'open_': Open.s,
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
        'rvi_length': rvi_length,
        'refined': refined,
        'thirds': thirds,
        'mamode': mamode,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.inertia(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = inertiaIndicator(data)
    print(data_indicator)