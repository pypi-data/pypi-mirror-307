from backtesting._util import _Data
import pandas_ta as ta


def rmaIndicator(data:_Data, length:int = 10):
    '''
    rmaIndicator(data:_Data, length:int = 10) -> pd.Series
    rmaIndicator(data:_Data, length:int = 10) -> Calcula el indicador RMA (Running Moving Average) de una serie de precios.
    
    data: _Data : Serie de precios OHLC para calcular el indicador.
    length: int : Numero de periodos a considerar para el calculo del indicador.
    
    return: pd.Series : Serie de datos del indicador calculado.
    '''
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
    }    
    
    rs = ta.rma(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = rmaIndicator(data)
    print(data_indicator)