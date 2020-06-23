# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
import numpy as np
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

#The below fucnt is callable with arguments: stock_price, window_size and number_of_std
def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std  = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, lower_band

class BinHV45(IStrategy):
    minimal_roi = {
        "0": 0.0125
    }

    stoploss = -0.05
    ticker_interval = '1m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        #below line calls the bollinger_band fucnt above
        mid, lower = bollinger_bands(dataframe['close'], window_size=40, num_of_std=2)
        dataframe['mid'] = np.nan_to_num(mid) #replace nan with zero
        dataframe['lower'] = np.nan_to_num(lower) #replace nan with zero
        dataframe['bbdelta'] = (dataframe['mid'] - dataframe['lower']).abs() #absolute delta between mid and lower bb bands
        dataframe['pricedelta'] = (dataframe['open'] - dataframe['close']).abs() #absolute delta between 
        dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
        dataframe['tail'] = (dataframe['close'] - dataframe['low']).abs()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                dataframe['lower'].shift().gt(0) &
                dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
                dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
                dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
                dataframe['close'].lt(dataframe['lower'].shift()) &
                dataframe['close'].le(dataframe['close'].shift())
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        no sell signal
        """
        dataframe['sell'] = 0
        return dataframe
