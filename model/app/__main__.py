# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.extract_data import ExtractData
from graph.plot_ import RawVisualization, RawHist2D, Correlation

from AI.train_val_split import TrainValSplit
from AI.datasets import TrainDataset, ValidationDataset
from AI.model import ModelTraining

from AI.test.single_step_prediction import show_plot

from arg_parse.arguments import args
# | Typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
from tensorflow.python.data.ops.batch_op import _BatchDataset
from keras.src.engine.functional import Functional as K_Functional
# |--------------------------------------------------------------------------------------------------------------------|

extract_data: ExtractData = ExtractData()
data: DataFrame = extract_data.read_csv()


if args.graph:
    raw_visualization: RawVisualization = RawVisualization()
    raw_visualization.define_data(data)
    raw_visualization.show()

if args.hist2d:
    raw_hist_2d: RawHist2D = RawHist2D()
    raw_hist_2d.define_data(data)
    raw_hist_2d.set_variables(args.hist2dx, args.hist2dy)
    raw_hist_2d.show()

if args.correlation:
    correlation: Correlation = Correlation()
    correlation.define_data(data)
    correlation.show_heatmap()

if args.AI:
    
    # TranValSplit Instance
    train_val_split: TrainValSplit = TrainValSplit(data)
    train, valid, feature = train_val_split.get()
    train_split: int = train_val_split.get_train_split_index()

    # TrainDataset Instance
    training_dataset: TrainDataset = TrainDataset(train)
    training_dataset.define_train_split(train_split)
    training_dataset.define_feature(feature)
    train_dataset: _BatchDataset = training_dataset.get()
    
    #ValidationDataset Instance
    validation_dataset: ValidationDataset = ValidationDataset(valid)
    validation_dataset.define_train_split(train_split)
    validation_dataset.define_feature(feature)
    valid_dataset: _BatchDataset = validation_dataset.get()
        
    # Model Traning
    model_training: ModelTraining = ModelTraining(train_dataset, valid_dataset)
    model_training.fit_model()

if args.AIprediction:
    # TranValSplit Instance
    train_val_split: TrainValSplit = TrainValSplit(data)
    train, valid, feature = train_val_split.get()
    train_split: int = train_val_split.get_train_split_index()

    # TrainDataset Instance
    training_dataset: TrainDataset = TrainDataset(train)
    training_dataset.define_train_split(train_split)
    training_dataset.define_feature(feature)
    train_dataset: _BatchDataset = training_dataset.get()
    
    #ValidationDataset Instance
    validation_dataset: ValidationDataset = ValidationDataset(valid)
    validation_dataset.define_train_split(train_split)
    validation_dataset.define_feature(feature)
    valid_dataset: _BatchDataset = validation_dataset.get()
    
    model: K_Functional = ModelTraining.load_model()
    
    # for x, y in valid_dataset.take(5):
    #     show_plot(
    #         plot_data=[x[0][:, 1].numpy(), y[0].numpy(), model.predict(x)[0]],
    #         delta=12,
    #         title="Single Step Prediction"
    #     )
    
    
    import numpy as np
    y_p: np.ndarray
    y  : np.ndarray
    
    for x, y in valid_dataset.take(1):
        y_p: np.ndarray = model.predict(x)
        y  : np.ndarray = y.numpy()
    
    error: np.ndarray = y - y_p
    
    print(error.mean(axis=0), error.std(axis=0))