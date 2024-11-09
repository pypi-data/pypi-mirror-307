from backtesting._util import _Data
import pandas_ta as ta


def cdl_patternIndicator(data:_Data, name:str = "all", scalar:float = 100, offset:int = 0):
    """
    Funcion que calcula el patron de velas
    :param data: _Data
    :param name: str
    :param scalar: float
    :param offset: int
    :return: pd.Series
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
        'name': name,
        'scalar': scalar,
        'offset': offset,
    }    
    
    rs = ta.cdl_pattern(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cdl_patternIndicator(data)
    print(data_indicator)