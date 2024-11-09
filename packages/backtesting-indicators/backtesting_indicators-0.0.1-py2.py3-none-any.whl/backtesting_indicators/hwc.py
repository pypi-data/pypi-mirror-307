from backtesting._util import _Data
import pandas_ta as ta


def hwcIndicator(data:_Data, na:float = 0.1, nb:float = 0.1, nc:float = 0.1, nd:float = 0.1, scaler:float = 1.0, channel_eval:bool = False):
    """
    hwcIndicator(data:_Data, na:float = 0.1, nb:float = 0.1, nc:float = 0.1, nd:float = 0.1, scaler:float = 1.0, channel_eval:bool = False)
    
    Hull Moving Average (HMA) is a more responsive moving average that reduces lag by using the weighted moving average (WMA) formula.
    
    Params:
        data (_Data): Dataset
        na (float): Number of periods for the short WMA
        nb (float): Number of periods for the long WMA
        nc (float): Number of periods for the final WMA
        nd (float): Number of periods for the final WMA
        scaler (float): Value to scale the indicator
        channel_eval (bool): If True, returns the channel values
        
    Returns:
        _Data: New feature generated.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'na': na,
        'nb': nb,
        'nc': nc,
        'nd': nd,
        'scaler': scaler,
        'channel_eval': channel_eval,
    }    
    
    rs = ta.hwc(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = hwcIndicator(data)
    print(data_indicator.df)