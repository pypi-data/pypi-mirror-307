from backtesting._util import _Data
import pandas_ta as ta



def squeeze_proIndicator(data:_Data, high:int, low:int, close:int, bb_length:int = 20, bb_std:float = 2, kc_length:int = 20, kc_scalar_wide:float = 2, kc_scalar_normal:float = 1.5, kc_scalar_narrow:float = 1, mom_length:int = 12, mom_smooth:int = 6, mamode:str = "sma", offset:int = 0, tr:bool = True, asint:bool = True, detailed:bool = False, fillna:bool = True, fill_method:str = "ffill"):
    pass

if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = squeeze_proIndicator(data, 'high', 'low', 'close')
    print(data_indicator)
