from backtesting._util import _Data
import pandas_ta as ta


def increasingIndicator(data:_Data, length:int = 1, strict:bool = False, percent:float = None, asint:bool = True, drift:int = 1, offset:int = 0, fillna=None, fill_method=None):
    """
    increasingIndicator(data:_Data, length:int = 1, strict:bool = False, percent:float = None, asint:bool = True, drift:int = 1, offset:int = 0, fillna=None, fill_method=None)
    
    Increasing Indicator
    Inputs:
        data: _Data
        length: int = 1
        strict: bool = False
        percent: float = None
        asint: bool = True
        drift: int = 1
        offset: int = 0
        fillna: None
        fill_method: None
    Outputs:
        pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'strict': strict,
        'percent': percent,
        'asint': asint,
        'drift': drift,
        'offset': offset,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.increasing(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = increasingIndicator(data)
    print(data_indicator)