from backtesting._util import _Data
import pandas_ta as ta




if __name__ == "__main__":
    import datetime
    from backtesting_data.history import historySymbol
    tmp = historySymbol('binanceusdm', 'ETH/USDT', '5m', 100, datetime.datetime(2024, 11, 6, 3))
    data = _Data(tmp)
    data_indicator = short_runIndicator(data)
    print(data_indicator)
    print(data_indicator['rsi'])
    print(data_indicator['rsi'].tail(5))
    print(data_indicator['rsi'].tail(5).iloc[0])
    print(data_indicator['rsi'].tail(5).iloc[0] > 70)
    print(data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 or data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail(5).iloc[0] < 30)
    print(data_indicator['rsi'].tail(5).iloc[0] > 70 and data_indicator['rsi'].tail