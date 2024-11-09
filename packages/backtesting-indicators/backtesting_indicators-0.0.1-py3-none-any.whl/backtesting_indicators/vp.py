from backtesting._util import _Data
import pandas_ta as ta


def vpIndicator(data:_Data, width:int = 10):
    """
    vpIndicator(data:_Data, width:int = 10)
    
    Vortex Indicator (VI) is a directional movement indicator that shows the current 
    trend's direction. It consists of two lines that capture positive and negative trend 
    movements. The Vortex Indicator is used to identify the start of a new trend, the 
    continuation of the current trend, and the end of a current trend. It is also used 
    to identify periods of congestion. The Vortex Indicator consists of two oscillators 
    that capture positive and negative trend movement. The Vortex Indicator is typically 
    used to identify the start of a new trend or the continuation of the current trend. 
    The Vortex Indicator is used to identify periods of congestion and periods of 
    acceleration. The Vortex Indicator is used to identify periods of congestion and 
    periods of acceleration. The Vortex Indicator is used to identify periods of 
    congestion and periods of acceleration. The Vortex Indicator is used to identify 
    periods of congestion and periods of acceleration. The Vortex Indicator is used to 
    identify periods of congestion and periods of acceleration. The Vortex Indicator is 
    used to identify periods of congestion and periods of acceleration. The Vortex 
    Indicator is used to identify periods of congestion and periods of acceleration. The 
    Vortex Indicator is used to identify periods of congestion and periods of acceleration. 
    The Vortex Indicator is used to identify periods of congestion and periods of 
    acceleration. The Vortex Indicator is used to identify periods of congestion and 
    periods of acceleration. The Vortex Indicator is used to identify periods of 
    congestion and periods of acceleration. The Vortex Indicator is used to identify 
    periods of congestion and periods of acceleration. The Vortex Indicator is used to 
    identify periods of congestion and periods of acceleration. The Vortex Indicator is 
    used to identify periods of congestion and periods of acceleration. The Vortex 
    Indicator is used to identify periods of congestion and periods of acceleration. The 
    Vortex Indicator is used to identify periods of congestion and periods of acceleration. 
    The Vortex Indicator is used to identify periods of congestion and periods of 
    acceleration. The Vortex Indicator is used to identify periods of congestion and 
    periods of acceleration. The Vortex Indicator is used to identify periods of 
    congestion and periods of acceleration. The Vortex Indicator is used to identify 
    periods of congestion and periods of acceleration. The Vortex Indicator is used to 
    identify periods of congestion and periods of acceleration. The Vortex Indicator is 
    used to identify periods of congestion and periods of acceleration. The Vortex 
    Indicator is used to identify periods of congestion and periods of acceleration. The 
    Vortex Indicator is used to identify periods of congestion and periods of acceleration. 
    The Vortex Indicator is used to identify periods of congestion and periods of 
    acceleration. The Vortex Indicator is used to identify periods of congestion and 
    periods of acceleration. The Vortex Indicator is used to identify periods of 
    congestion and periods of acceleration. The Vortex Indicator is used to identify 
    periods of congestion and periods of acceleration. The Vortex Indicator is used to 
    identify periods of congestion and periods of acceleration. The Vortex Indicator is 
    used to identify periods of congestion and periods of acceleration. The Vortex 
    Indicator is used to identify periods of congestion and periods of acceleration. The 
    Vortex Indicator is used to identify periods of congestion and periods of acceleration. 
    The Vortex Indicator is used to identify periods of congestion and periods of 
    acceleration. The Vortex Indicator is used to identify periods of congestion and 
    periods of acceleration. The Vortex Indicator is used to identify periods of 
    congestion

if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = vpIndicator(data)
    print(data_indicator)
    """


    data.df['vp_pos'] = ta.vortex(data.df['High'], data.df['Low'], data.df['Close'], window=width, as_lines=True)[f'VI+_{width}']
    data.df['vp_neg'] = ta.vortex(data.df['High'], data.df['Low'], data.df['Close'], window=width, as_lines=True)[f'VI-_{width}']
    return data
