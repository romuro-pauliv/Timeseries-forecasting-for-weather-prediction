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

from keras.src.engine.keras_tensor  import KerasTensor      as K_KerasTensor
from keras.src.engine.functional    import Functional       as K_Functional
from keras.src.callbacks            import EarlyStopping    as K_EarlyStopping
from keras.src.callbacks            import ModelCheckpoint  as K_ModelCheckpoint
# |--------------------------------------------------------------------------------------------------------------------|

class ModelTrainingLog:
    @staticmethod
    def _set_model() -> None:
        LogConnectInstance.report("SET", "LOCAL", "info", True, "KERAS MODEL")
    
    @staticmethod
    def _set_checkpoint(path_: str) -> None:
        LogConnectInstance.report("SET", "LOCAL", "info", True, f"CHECKPOINT in [{path_}]")

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

        
        self.epochs         :   int     = int(MODELARGS['AI']['epochs'])
        self.LSTM_layer1    :   int     = int(MODELARGS['AI']['LSTM_layer1'])
        self.learning_rate  :   float   = float(MODELARGS['AI']['learning_rate'])
        self.loss_function  :   str     = MODELARGS['AI']['loss_function']
        self.path_checkpoint:   str     = MODELARGS['AI']['path_checkpoint']
        
        self.es_monitor_1   :   str     = MODELARGS['AI']['monitor_1']
        self.es_min_delta   :   int     = 0
        self.es_patience    :   int     = 5
        
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

        self.model: K_Functional = keras.Model(inputs=inputs, outputs=outputs)
        self.model.compile(optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate), loss=self.loss_function)
        
        ModelTrainingLog._set_model()
        self.model.summary()
    
    def _set_checkpoint(self) -> None:
        self.es_callback: K_EarlyStopping = keras.callbacks.EarlyStopping(
            monitor=self.es_monitor_1, min_delta=self.es_min_delta, patience=self.es_patience)
        
        self.modelckpt_callback: K_ModelCheckpoint = keras.callbacks.ModelCheckpoint(
            monitor=self.es_monitor_1,
            filepath=self.path_checkpoint,
            verbose=1,
            save_weights_only=True,
            save_best_only=True
        )
        
        ModelTrainingLog._set_checkpoint(self.path_checkpoint)
    
    def fit_model(self) -> None:
        self._set_model()
        self._set_checkpoint()
        
        history = self.model.fit(
            self.train_dataset, epochs=self.epochs,
            validation_data=self.valid_dataset, callbacks=[self.es_callback, self.modelckpt_callback]
        )