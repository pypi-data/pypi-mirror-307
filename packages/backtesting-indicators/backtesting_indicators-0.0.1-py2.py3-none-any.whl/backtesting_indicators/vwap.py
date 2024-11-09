from backtesting._util import _Data
import pandas_ta as ta


def vwapIndicator(data:_Data, anchor:str = "D", offset:int = 0):
    """
    VWAP (Volume Weighted Average Price) es un indicador que se calcula sumando el valor negociado (precio * volumen) y dividiendo por el volumen total negociado en un periodo determinado.
    El VWAP se utiliza para determinar el valor medio ponderado por volumen de un activ

if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = vwapIndicator(data)
    print(data_indicator)
    """
    data.df['vwap'] = ta.vwap(data.df['close'], data.df['volume'])
    return data
