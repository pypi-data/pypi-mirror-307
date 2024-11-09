from backtesting._util import _Data
import pandas_ta as ta


def pvtIndicator(data:_Data, drift:int = 1, offset:int = 0):
    """
    pvtIndicator(data:_Data, drift:int = 1, offset:int = 0)
    
    PVT (Price Volume Trend) es un indicador basado en el volumen y el precio

if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = pvtIndicator(data)
    print(data_indicator)
    """
    data.data['pvt'] = ta.pvt(data.data['close'], data.data['volume'], drift=drift, offset=offset)
    return data
