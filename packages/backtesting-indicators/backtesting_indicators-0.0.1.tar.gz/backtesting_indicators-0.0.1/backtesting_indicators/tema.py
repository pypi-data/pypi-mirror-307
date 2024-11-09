from backtesting._util import _Data
import pandas_ta as ta


def temaIndicator(data:_Data, length:int = 10):
    '''
    temaIndicator(data:_Data, length:int = 10)
    
    data: _Data
    length: int
    
    return: pd.Series
    '''
    Close = data.Close
            
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.tema(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = temaIndicator(data)
    print(data_indicator)