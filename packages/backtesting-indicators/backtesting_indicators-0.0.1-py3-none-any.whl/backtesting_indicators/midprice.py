from backtesting._util import _Data
import pandas_ta as ta


def midpriceIndicator(data:_Data, length:int = 10):
    """
    midpriceIndicator(data:_Data, length:int = 10)
    
    Funcion que recibe un objeto de tipo _Data y un entero, y devuelve un objeto de tipo _Data con la columna midprice.
    
    Parametros:
    data : _Data : Objeto de tipo _Data
    length : int : Entero que indica el periodo de tiempo
    
    Retorna:
    _Data : Objeto de tipo _Data con la columna midprice
    """
    High = data.High
    Low = data.Low
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'length': length,
    }    
    
    rs = ta.midprice(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = midpriceIndicator(data)
    print(data_indicator.df)