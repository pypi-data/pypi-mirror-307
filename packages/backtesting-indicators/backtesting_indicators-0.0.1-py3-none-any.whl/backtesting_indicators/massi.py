from backtesting._util import _Data
import pandas_ta as ta


def massiIndicator(data:_Data, fast:int = 9, slow:int = 25, offset:int = 0):
    """
    massiIndicator(data:_Data, fast:int = 9, slow:int = 25, offset:int = 0)
    
    Funcion que calcula el Mass Index
    


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = massiIndicator(data)
    print(data_indicator)
    """    
    data.df['massi'] = ta.massi(data.df['high'], data.df['low'], fast=fast, slow=slow)
    return data.df['massi']