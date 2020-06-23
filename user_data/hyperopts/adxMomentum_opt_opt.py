# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa
import talib.abstract as ta  # noqa
from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
# Add your lib to import here

import freqtrade.vendor.qtpylib.indicators as qtpylib


class adxMomentum_opt_opt(IHyperOpt):
    """
    This is a sample Hyperopt to inspire you.
    More information in the documentation: https://www.freqtrade.io/en/latest/hyperopt/
    You should:
    - Rename the class name to some unique name.
    - Add any methods you want to build your hyperopt.
    - Add any lib you need to build your hyperopt.
    An easier way to get a new hyperopt file is by using
    `freqtrade new-hyperopt --hyperopt MyCoolHyperopt`.
    You must keep:
    - The prototypes for the methods: populate_indicators, indicator_space, buy_strategy_generator.
    The methods roi_space, generate_roi_table and stoploss_space are not required
    and are provided by default.
    However, you may override them if you need 'roi' and 'stoploss' spaces that
    differ from the defaults offered by Freqtrade.
    Sample implementation of these methods will be copied to `user_data/hyperopts` when
    creating the user-data directory using `freqtrade create-userdir --userdir user_data`,
    or is available online under the following URL:
    https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_hyperopt_advanced.py.
    """

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        dataframe['sar'] = ta.SAR(dataframe)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by Hyperopt.
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use.
            """
            conditions = []

            # GUARDS AND TRENDS         
            if 'adx-enabled' in params and params['adx-enabled']:
                conditions.append(dataframe['adx'] > params['adx-value'])
            if 'mom-enabled' in params and params['mom-enabled']:
                conditions.append(dataframe['mom'] < params['mom-value'])
            if 'minus_di-enabled' in params and params['minus_di-enabled']:
                conditions.append(dataframe['minus_di'] > params['minus_di-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'minus_di':
                    conditions.append(dataframe['plus_di'] < dataframe['minus_di'])

                    

            # Check that volume is not 0
            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
    
            Integer(15, 50, name='adx-value'),
            Categorical([True, False], name='adx-enabled'),
            Integer(-10, 10, name='mom-value'),
            Categorical([True, False], name='mom-enabled'),
            Integer(40, 65, name='minus_di-value'),
            Categorical([True, False], name='minus_di-enabled')
            
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use.
            """
            conditions = []
            
            # GUARDS AND TRENDS         
            if 'adx-enabled' in params and params['adx-enabled']:
                conditions.append(dataframe['adx'] > params['adx-value'])
            if 'mom-enabled' in params and params['mom-enabled']:
                conditions.append(dataframe['mom'] > params['mom-value'])
            if 'minus_di-enabled' in params and params['minus_di-enabled']:
                conditions.append(dataframe['minus_di'] > params['minus_di-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'minus_di':
                    conditions.append(dataframe['plus_di'] > dataframe['minus_di'])
                    

            # Check that volume is not 0
            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            
            Integer(15, 50, name='adx-value'),
            Categorical([True, False], name='adx-enabled'),
            Integer(-10, 10, name='mom-value'),
            Categorical([True, False], name='mom-enabled'),
            Integer(40, 65, name='minus_di-value'),
            Categorical([True, False], name='minus_di-enabled')

        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include buy space.
        """
        dataframe.loc[
            (
                    (dataframe['mom'] < 0) &
                    (dataframe['minus_di'] > 48) &
                    (dataframe['plus_di'] < dataframe['minus_di'])

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include sell space.
        """
        dataframe.loc[
            (
                    (dataframe['mom'] > 0) &
                    (dataframe['minus_di'] > 48) &
                    (dataframe['plus_di'] > dataframe['minus_di'])

            ),
            'sell'] = 1
        
        return dataframe