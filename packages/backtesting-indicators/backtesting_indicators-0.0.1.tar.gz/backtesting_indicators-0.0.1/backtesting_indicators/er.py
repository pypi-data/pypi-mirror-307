from backtesting._util import _Data
import pandas_ta as ta


def erIndicator(data:_Data, length:int = 10):
    '''
    erIndicator(data:_Data, length:int = 10)
    
    Esta funcion recibe un objeto de tipo _Data y un entero, y devuelve un objeto de tipo _Data.
    
    data: Es un objeto de tipo _Data que contiene los datos de un activo financiero.
    
    length: Es un entero que representa el periodo de tiempo.
    
    return: Un objeto de tipo _Data con los datos del indicador ER.
    '''
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.er(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = erIndicator(data)
    print(data_indicator.df)
