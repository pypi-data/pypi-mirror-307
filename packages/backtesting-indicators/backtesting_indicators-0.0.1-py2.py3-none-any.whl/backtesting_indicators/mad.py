from backtesting._util import _Data
import pandas_ta as ta


def madIndicator(data:_Data, length:int = 30):
    '''
    madIndicator(data:_Data, length:int = 30)
    
    Funcion que calcula el Mean Absolute Deviation de un conjunto de datos
    
    Parametros:
    data : _Data : Dataframe con los datos
    length : int : Longitud de la ventana
    
    Retorna:
    rs : pd.Series : Serie con el resultado del indicador
    '''
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.mad(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = madIndicator(data)
    print(data_indicator)