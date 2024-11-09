from backtesting._util import _Data
import pandas_ta as ta


def td_seqIndicator(data:_Data, asint:bool = False, offset:int = 0, show_all:bool = True, fillna:float = None):
    """
    td_seqIndicator(data:_Data, asint:bool = False, offset:int = 0, show_all:bool = True, fillna:float = None)
    
    TD Sequential (TD Seq) is a momentum indicator developed by market timer Tom DeMark. The purpose of the indicator is to identify a price point where an uptrend or a downtrend exhausts itself and reverses. The indicator consists of two parts: TD Setup and TD Countdown. The TD Setup helps identify when a price move is starting, while TD Countdown helps identify when a price move is coming to an end. The indicator is used to identify when a price is overextended in one direction and is likely to reverse.
    
    Params:
    data: _Data: Data
    asint: bool: default False
    offset: int: default 0
    show_all: bool: default True
    fillna: float: default None
    
    Returns:
    rs: pd.Series
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'asint': asint,
        'offset': offset,
        'show_all': show_all,
        'fillna': fillna
    }    
    
    rs = ta.td_seq(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = td_seqIndicator(data)
    print(data_indicator)