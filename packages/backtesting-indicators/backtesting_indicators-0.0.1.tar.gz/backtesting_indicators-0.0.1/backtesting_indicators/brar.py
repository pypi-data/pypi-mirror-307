from backtesting._util import _Data
import pandas_ta as ta


def brarIndicator(data:_Data, length:int = 26, scalar:float = 100, drift:int = 1, offset:int = 0):
    """
    brarIndicator(data:_Data, length:int = 26, scalar:float = 100, drift:int = 1, offset:int = 0)
    
    BRAR (Buy/Sell Pressure) is a range-bound oscillator that fluctuates between -100 and 100.
    It is designed to identify the buying and selling pressure in the market.
    
    Params:
    data: _Data : Data
    length: int : The length of the RSI. Default: 26
    scalar: float : A scalar to multiply the RSI. Default: 100
    drift: int : The drift of the RSI. Default: 1
    offset: int : The offset of the RSI. Default: 0
    
    Returns:
    rs : pd.Series
    """
    open_ = data.Open
    high = data.High
    low = data.Low
    close = data.Close
    
    attr = {
        'open_': open_.s,
        'high': high.s,
        'low': low.s,
        'close': close.s,
        'length': length,
        'scalar': scalar,
        'drift': drift,
        'offset': offset,
    }
    
    rs = ta.brar(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = brarIndicator(data)
    print(data_indicator)
