from backtesting._util import _Data
import pandas_ta as ta


def adoscIndicator(data:_Data, fast:int = 12, slow:int = 26):
    """
    ADOSC - Accumulation/Distribution Oscillator
    Formula:
    ADOSC = SUM((Close - Open) / (High - Low) * Volume, fast) / SUM((Close - Open) / (High - Low) * Volume, slow)
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    Open = data.Open
    Volume = data.Volume
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'open': Open.s,
        'volume': Volume.s,
        'fast': fast,
        'slow': slow,
    }    
    
    rs = ta.adosc(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = adoscIndicator(data)
    print(data_indicator)