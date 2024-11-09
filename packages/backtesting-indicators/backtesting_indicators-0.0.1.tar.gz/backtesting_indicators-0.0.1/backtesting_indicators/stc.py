from backtesting._util import _Data
import pandas_ta as ta


def stcIndicator(data:_Data, tclen:int = 10, fast:int = 12, slow:int = 26, factor:float = 0.5, offset:int = 0):
    """
    stcIndicator(data:_Data, tclen:int = 10, fast:int = 12, slow:int = 26, factor:float = 0.5, offset:int = 0)
    
    STC (Stochastic Oscillator) Indicator
    
    Parametros:
    data: _Data : Data Class
    tclen: int : Time period for the center line
    fast: int : Time period for the fast line
    slow: int : Time period for the slow line
    factor: float : Factor for smoothing
    offset: int : Offset
    
    Retorna:
    rs : pd.Series : Result
    """
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'tclen': tclen,
        'fast': fast,
        'slow': slow,
        'factor': factor,
        'offset': offset,
    }    
    
    rs = ta.stc(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = stcIndicator(data)
    print(data_indicator)