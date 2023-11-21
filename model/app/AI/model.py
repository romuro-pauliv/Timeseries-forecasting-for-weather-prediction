# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 app.model.model.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data import MODELARGS

from connections.log import LogConnectInstance

import keras
# | Typing |-----------------------------------------------------------------------------------------------------------|
from tensorflow.python.data.ops.batch_op import _BatchDataset

from keras.src.engine.keras_tensor import KerasTensor as K_KerasTensor
from keras.src.engine.functional import Functional as K_Functional
# |--------------------------------------------------------------------------------------------------------------------|

class ModelTrainingLog:
    @staticmethod
    def _set_model() -> None:
        LogConnectInstance.report("SET", "LOCAL", "info", True, "KERAS MODEL")

class ModelTraining(object):
    def __init__(self, train_dataset: _BatchDataset, valid_dataset: _BatchDataset) -> None:
        """
        Initialize ModelTraining
        Args:
            train_dataset (_BatchDataset): Tensor to traning model
            valid_dataset (_BatchDataset): Tensor to valid model
        """
        self.train_dataset: _BatchDataset = train_dataset
        self.valid_dataset: _BatchDataset = valid_dataset

        self.LSTM_layer1: int = int(MODELARGS['AI']['LSTM_layer1'])
        
        self.learning_rate: float = float(MODELARGS['AI']['learning_rate'])
        self.loss_function: str   = MODELARGS['AI']['loss_function']
        
        self._get_batch_data()
        
    def _get_batch_data(self) -> None:
        """
        Fetches a batch of data for model initialization.
        """
        for batch in self.train_dataset.take(1):
            self.inputs_data, self.target_data = batch
    
    def _set_model(self) -> None:
        """
        Sets up the model architecture and compiles it.
        """
        inputs  : K_KerasTensor = keras.layers.Input(shape=(self.inputs_data.shape[1], self.inputs_data.shape[2]))
        lstm_out: K_KerasTensor = keras.layers.LSTM(self.LSTM_layer1)(inputs)
        outputs : K_KerasTensor = keras.layers.Dense(1)(lstm_out)

        model: K_Functional = keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate), loss=self.loss_function)
        
        ModelTrainingLog._set_model()
        model.summary()