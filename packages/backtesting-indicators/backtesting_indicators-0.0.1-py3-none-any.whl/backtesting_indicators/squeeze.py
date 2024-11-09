from backtesting._util import _Data
import pandas_ta as ta


def squeezeIndicator(data:_Data, bb_length:int = 20, bb_std:float = 2, kc_length:int = 20, kc_scalar:float = 1.5, mom_length:int = 12, mom_smooth:int = 6, mamode:str = "sma", offset:int = 0, tr:bool = True, asint:bool = True, lazybear:bool = False, detailed:bool = False, fillna:bool = True, fill_method:str = "ffill"):
    """
    Squeeze Indicator

    Squeeze Indicator is a volatility-based indicator that identifies periods of consolidation in a market. It is constructed with Bollinger Bands and Keltner Channels. When the Bollinger Bands (BB) are inside the Keltner Channels (KC), a market squeeze occurs and a signal is issued. A Squeeze is defined as the BB having gone within the KC and then exited the KC. The signal is plotted as histogram above and below a zero line. When the histogram is above the zero line, it means that the Bollinger Bands are within the Keltner Channels and the market is consolidating. When the histogram is below the zero line, it means that the Bollinger Bands have exited the Keltner Channels and the market is trending.

    Note: The Squeeze Indicator is not a directional indicator. It is a volatility indicator. It is designed to go long or short based on the breakout direction. For example, if the histogram is above the zero line, longs are taken. If the histogram is below the zero line, shorts are taken.

    Args:
        data (pd.DataFrame): DataFrame which contain ['high', 'low', 'close'] columns.
        bb_length (int): The time period for the Bollinger Bands.
        bb_std (float): The standard deviation for the Bollinger Bands.
        kc_length (int): The time period for the Keltner Channels.
        kc_scalar (float): The scalar for the Keltner Channels.
        mom_length (int): The time period for the Momentum.
        mom_smooth (int): The time period for the Momentum moving average.
        mamode (str): The moving average mode for the Momentum. Options are ['sma', 'ema', 'wma', 'dema', 'tema', 'trima', 'trix', 'vama'].
        offset (int): How many periods to offset the result. Negative value means that the indicator will be shifted to the left.
        tr (bool): If True, use True Range for calculations.
        asint (bool): If True, returns the as integer values.
        lazybear (bool): If True, use the LazyBear squeeze implementation.
        detailed (bool): If True, returns the detailed output.
        fillna (bool): If True, fill NaN values.
        fill_method (str): Method for filling NaN values. See pandas.DataFrame.fillna.

    Returns:
        pd.DataFrame: A DataFrame with original inputs and the squeeze indicator.
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'bb_length': bb_length,
        'bb_std': bb_std,
        'kc_length': kc_length,
        'kc_scalar': kc_scalar,
        'mom_length': mom_length,
        'mom_smooth': mom_smooth,
        'mamode': mamode,
        'offset': offset,
        'tr': tr,
        'asint': asint,
        'lazybear': lazybear,
        'detailed': detailed,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.squeeze(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = squeezeIndicator(data)
    print(data_indicator)
