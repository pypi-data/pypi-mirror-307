from backtesting._util import _Data
import pandas_ta as ta


def rsiIndicator(data:_Data, length:int = 14, scalar:float = 100, drift:int = 1):
    """
    Relative Strength Index (RSI)
    
    The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. 
    The RSI oscillates between 0 and 100. Traditionally the RSI is considered overbought when above 70 and oversold when below 30.
    
    Args:
        data (_Data): Dataset
        length (int): Period to consider
        scalar (float): Scalar to multiply
        drift (int): Drift
    
    Returns:
        rs (pd.Series): Resulting RSI
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'scalar': scalar,
        'drift': drift,
    }    
    
    rs = ta.rsi(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = rsiIndicator(data)
    print(data_indicator)