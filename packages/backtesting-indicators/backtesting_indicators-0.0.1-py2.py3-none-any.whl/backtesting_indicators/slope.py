from backtesting._util import _Data
import pandas_ta as ta


def slopeIndicator(data:_Data, length:int = 1, offset:int = 0, as_angle:bool = False, to_degrees:bool = False, fillna:bool = False, fill_method:str = 'pad'):
    """
    slopeIndicator(data:_Data, length:int = 1, offset:int = 0, as_angle:bool = False, to_degrees:bool = False, fillna:bool = False, fill_method:str = 'pad')
    
    Slope Indicator
    Inputs:
      data: _Data
      length: int = 1
      offset: int = 0
      as_angle: bool = False
      to_degrees: bool = False
      fillna: bool = False
      fill_method: str = 'pad'
    Outputs:
      rs: pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'offset': offset,
        'as_angle': as_angle,
        'to_degrees': to_degrees,
        'fillna': fillna,
        'fill_method': fill_method
    }    
    
    rs = ta.slope(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = slopeIndicator(data)
    print(data_indicator)