from backtesting._util import _Data
import pandas_ta as ta

def tsignalsIndicator(data:_Data, trend, asbool=False, trend_reset=0, trade_offset=0, drift=1):
    """
    tsignalsIndicator(data:_Data, trend, asbool=False, trend_reset=0, trade_offset=0, drift=1)
    
    Tsignals Indicator
    
    Params:
    - data: Data
    - trend: Trend
    - asbool: Asbool
    - trend_reset: Trend Reset
    - trade_offset: Trade Offset
    - drift: Drift
    
    Returns:
    - rs
    """
    attr = {
        'trend': trend,
        'asbool': asbool,
        'trend_reset': trend_reset,
        'trade_offset': trade_offset,
        'drift': drift,
    }
    
    rs = ta.tsignals(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = tsignalsIndicator(data, trend=0, asbool=False, trend_reset=0, trade_offset=0, drift=1)
    print(data_indicator)