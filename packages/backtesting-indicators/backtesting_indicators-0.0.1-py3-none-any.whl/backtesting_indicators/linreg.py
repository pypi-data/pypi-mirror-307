from backtesting._util import _Data
import pandas_ta as ta


def linregIndicator(data:_Data, length:int = 10, angle:bool = False, degrees:bool = False, intercept:bool = False, r:bool = False, slope:bool = False, tsf:bool = False, fillna:float = None, fill_method:str = None):
    """
    linregIndicator(data:_Data, length:int = 10, angle:bool = False, degrees:bool = False, intercept:bool = False, r:bool = False, slope:bool = False, tsf:bool = False, fillna:float = None, fill_method:str = None)
    
    Funcion que calcula el indicador de regresion lineal.
    
    Parametros:
    - data: Dataframe con los datos de entrada.
    - length: Numero de periodos.
    - angle: Si se quiere el angulo.
    - degrees: Si se quiere en grados.
    - intercept: Si se quiere la interseccion.
    - r: Si se quiere el coeficiente de correlacion.
    - slope: Si se quiere la pendiente.
    - tsf: Si se quiere el factor de tiempo.
    - fillna: Valor para llenar los datos faltantes.
    - fill_method: Metodo para llenar los datos faltantes.
    
    Retorna:
    - Dataframe con el indicador de regresion lineal.
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'length': length,
        'angle': angle,
        'degrees': degrees,
        'intercept': intercept,
        'r': r,
        'slope': slope,
        'tsf': tsf,
        'fillna': fillna,
        'fill_method': fill_method,
    }    
    
    rs = ta.linreg(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = linregIndicator(data)
    print(data_indicator)