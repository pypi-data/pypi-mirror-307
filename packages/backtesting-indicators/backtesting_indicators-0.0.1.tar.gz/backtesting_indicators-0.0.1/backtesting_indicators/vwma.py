from backtesting._util import _Data
import pandas_ta as ta

def vwmaIndicator(data:_Data, length:int = 10):
    """
    VWMA (Volume Weighted Moving Average) is a simple moving average that considers the volume traded in a period. 
    The indicator is calculated by taking the sum of the product of the volume and the price and then dividing this sum by the total volume.
    VWMA = (Sum(volume * price) / Sum(volume))
    """
    Close = data.Close
    Volume = data.Volume
    
    attr = {
        'close': Close.s,
        'volume': Volume.s,
        'length': length,
    }    
    
    rs = ta.vwma(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = vwmaIndicator(data)
    print(data_indicator)
