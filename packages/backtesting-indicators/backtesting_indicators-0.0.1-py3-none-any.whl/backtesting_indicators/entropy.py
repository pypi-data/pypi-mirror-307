from backtesting._util import _Data
import pandas_ta as ta


def entropyIndicator(data:_Data, length:int = 10, base:float = 2):
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'base': base,
    }    
    
    rs = ta.entropy(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = entropyIndicator(data)
    print(data_indicator)