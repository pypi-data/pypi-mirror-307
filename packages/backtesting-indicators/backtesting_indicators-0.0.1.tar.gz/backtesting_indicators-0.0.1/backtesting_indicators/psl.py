from backtesting._util import _Data
import pandas_ta as ta


def pslIndicator(data:_Data, length:int = 12, scalar:float = 100, drift:int = 1, offset:int = 0):
    """
    pslIndicator(data:_Data, length:int = 12, scalar:float = 100, drift:int = 1, offset:int = 0)
    
    Price and Volume Trend (PVT) is a technical analysis indicator intended to relate price and volume in the stock market.
    PVT is based on a running total volume, with volume added or subtracted according to the percentage change of the closing price today over the closing price yesterday.
    
    source: https://www.investopedia.com/terms/p/pricvolumetrend.asp
    
    params:
    data: _Data : Data Class Object
    length: int : 12
    scalar: float : 100
    drift: int : 1
    offset: int : 0
    
    return:
    rs : pd.Series
    """
    Close = data.Close
    Open = data.Open
    
    attr = {
        'close': Close.s,
        'open_': Open.s,
        'length': length,
        'scalar': scalar,
        'drift': drift,
        'offset': offset,
    }    
    
    rs = ta.psl(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pslIndicator(data)
    print(data_indicator)