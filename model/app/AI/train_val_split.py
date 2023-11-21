# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       app.model.train_val_split.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|
# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.log import LogConnectInstance

from resources.data import SELECT_VARIABLES, MODELARGS

from graph.resources.variables_names import feature_keys, titles, date_time_key

from AI.normalization import normalize

import numpy as np
import pandas as pd
# | typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
from pandas.core.series import Series
# |--------------------------------------------------------------------------------------------------------------------|

class TrainValSplitLog:
    @staticmethod
    def _select_variables(var_name: str) -> None:
        LogConnectInstance.report("SELECT", "LOCAL", "info", True, f"[{var_name}]")
    
    @staticmethod
    def _make_new_feature_dataframe() -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True, "NEW DATAFRAME")

    @staticmethod
    def _get_split_fraction(split_fraction: float, train_split_data: int) -> None:
        split_fraction: float = round(split_fraction*100, 2)
        LogConnectInstance.report("GET", "LOCAL", "info", True, f"TRAIN SPLIT [{split_fraction}%] [{train_split_data}]")

class TrainValSplit(object):
    def __init__(self, data: DataFrame) -> None:
        """
        Intialize TranValSplit instance.
        """
        self.data: DataFrame = data
        
        self.split_fraction:    float     = float(MODELARGS['train_val_data']['split_fraction'])
        self.date_time_key:     str       = date_time_key
        self.features_keys:     list[str] = feature_keys
        self.titles:            list[str] = titles
        
        self.select_variables: list[int] = SELECT_VARIABLES['select_variables']
        self.select_features : list[str] = [self.features_keys[i] for i in self.select_variables]
        
        self._log_select_variables()
        self._get_split_fraction()
    
    def _get_split_fraction(self) -> None:
        """
        Get Index to split dataset in train and validation
        """
        self.train_split: int = int(self.split_fraction * int(self.data.shape[0]))
        TrainValSplitLog._get_split_fraction(self.split_fraction, self.train_split)
    
    def _log_select_variables(self) -> None:
        """
        Send log of the selected variables
        """
        for i in self.select_variables:
            TrainValSplitLog._select_variables(self.titles[i])
    
    def _make_new_feature_dataframe(self) -> None:
        """
        Create new dataframe with only selected variables
        """
        self.features:          DataFrame    = self.data[self.select_features]
        self.features.index:    Series       = self.data[self.date_time_key]
        print(self.features.head())
        TrainValSplitLog._make_new_feature_dataframe()
    
    def _normalize_feature(self) -> None:
        """
        Normalize the dataset
        """
        self.features: np.array = normalize(self.features.values, self.train_split)
        self.features: DataFrame = pd.DataFrame(self.features)
        print(self.features.head())
    
    def get(self) -> tuple[DataFrame, DataFrame]:
        """
        Return Train and Valid Dataset
        Returns:
            tuple[DataFrame, DataFrame]: (train, valid) datasets
        """
        self._make_new_feature_dataframe()
        self._normalize_feature()
    
        return self.features[0:self.train_split-1], self.features[self.train_split:], self.features
    
    def get_train_split_index(self) -> int:
        """
        Return train_split var(int)
        Returns:
            int: train_split variable
        """
        return self.train_split