from backtesting._util import _Data
import pandas_ta as ta


def ohlc4Indicator(data:_Data):
    """
    ohlc4Indicator(data:_Data) -> pd.Series

    ohlc4Indicator es una funcion que recibe un objeto de tipo _Data y devuelve un objeto de tipo pd.Series

    Parametros:
    data: _Data -> Un objeto de tipo _Data que contiene los datos necesarios para calcular el indicador

    Retorna:
    pd.Series -> Un objeto de tipo pd.Series que contiene el resultado del indicador calculado
    """
    Open = data.Open
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'open': Open.s,
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
    }    
    
    rs = ta.ohlc4(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = ohlc4Indicator(data)
    print(data_indicator)
