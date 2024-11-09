from backtesting._util import _Data
import pandas_ta as ta


def cross_valueIndicator(data:_Data):
    """
    Esta funcion calcula la diferencia entre el precio de cierre y el precio de apertura de una vela
    """
    data['cross_valueIndicator'] = data['close'] - data['open']
    return data


if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = cross_valueIndicator(data)
    print(data_indicator)