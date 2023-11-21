# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              app.model.datasets.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.log import LogConnectInstance

from resources.data import MODELARGS

import keras
import numpy as np
# | Typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
# |--------------------------------------------------------------------------------------------------------------------|


class TrainDatasetLog:
    @staticmethod
    def _define_xy() -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True, "[TRAIN] - X & Y DATASET")
    
    @staticmethod
    def _define_timeseries_from_array() -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True,
                                  "[TRAIN] - keras.preprocessing.timeseries_dataset_from_array")

class TrainDataset(object):
    def __init__(self, train_data: DataFrame) -> None:
        """
        Initalize TrainDataset instance.
        Args:
            train_data (DataFrame): Normalized train dataframe
        """
        self.train_data: DataFrame = train_data
        
        self.split_fraction: float = float(MODELARGS['train_val_data']['split_fraction'])
        
        self.y_index    : int = int(MODELARGS['AI']['y_index'])
        self.step       : int = int(MODELARGS['AI']['step'])
        self.batch_size : int = int(MODELARGS['AI']['batch_size'])
                
        self.past   : int = int(MODELARGS['timeseries_config']['past'])
        self.future : int = int(MODELARGS['timeseries_config']['future'])
        
        self.n_columns: int = len(self.train_data.columns)
        
    def define_train_split(self, train_split: int) -> None:
        """
        Define train_split variable
        Args:
            train_split (int): Variable from train_val_split instance.
        """
        self.train_split: int = train_split
    
    def define_feature(self, feature: DataFrame) -> None:
        """
        Define feature (all data without split in train/valid dataset)
        Args:
            feature (DataFrame): Dataframe from train_val_split instance.
        """
        self.feature: DataFrame = feature
    
    def _define_xy(self) -> None:
        """
        Defines the X and Y variables for the dataset.
        """
        start: int = self.past + self.future
        end  : int = start + self.train_split
        
        self.x_train: np.ndarray  = self.train_data[[i for i in range(self.n_columns)]].values
        self.y_train: DataFrame   = self.feature.iloc[start:end][[1]]
        
        self.sequence_length: int = int(self.past / self.step)
        
        TrainDatasetLog._define_xy()

    def _define_timeseries_from_array(self) -> None:
        """
        Defines the time series dataset from arrays.
        """
        self.dataset_train = keras.preprocessing.timeseries_dataset_from_array(
            self.x_train, self.y_train,
            sequence_length=self.sequence_length,
            sampling_rate=self.step,
            batch_size=self.batch_size
        )
        
        TrainDatasetLog._define_timeseries_from_array()
    
    def get(self) -> keras.preprocessing.timeseries_dataset_from_array:
        """
        Obtains the time series dataset.
        Returns:
            keras.preprocessing.timeseries_dataset_from_array: timeseries dataset
        """
        self._define_xy()
        self._define_timeseries_from_array()
        return self.dataset_train