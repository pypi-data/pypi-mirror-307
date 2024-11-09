from backtesting._util import _Data
import pandas_ta as ta


def below_valueIndicator(data:_Data, value:int = 0):
    '''
    below_valueIndicator(data:_Data, value:int = 0)
    
    This function is a wrapper for the below_value function of the ta module.
    
    Parameters:
    data : _Data : The data to be used in the calculation.
    value : int : The value to be compared with the data.
    
    Returns:
    pd.Series : A series with the values of 1 when the data is below the value and 0 when it is not.
    '''
    
    Close = data.Close
    
    attr = {
        'close': Close.s,
        'value': value,
    }    
    
    rs = ta.below_value(**attr)

    return rs



if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = below_valueIndicator(data)
    print(data_indicator)