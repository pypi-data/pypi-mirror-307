from backtesting._util import _Data
import pandas_ta as ta


def willrIndicator(data:_Data, length:int = 20):
    """
    willrIndicator(data:_Data, length:int = 20) -> pd.Series
    willrIndicator(data:_Data, length:int) es una funciÃ³n que recibe un objeto de tipo _Data y un entero length, y devuelve una serie de pandas con el indicador Williams %R.
    
    ParÃ¡metros:
    data: Es un objeto de tipo _Data que contiene los datos necesarios para calcular el indicador.
    length: Es un entero que representa el periodo de tiempo a considerar en el cÃ¡lculo del indicador.
    
    Retorna:
    Un objeto de tipo pd.Series con el indicador Williams %R.
    """
    High = data.High
    Low = data.Low
    Close = data.Close
    
    attr = {
        'high': High.s,
        'low': Low.s,
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.willr(**attr)

    return rs


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = willrIndicator(data)
    print(data_indicator)