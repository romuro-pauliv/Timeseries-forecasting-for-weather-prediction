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

from arg_parse.arguments import args
# | Typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
from tensorflow.python.data.ops.batch_op import _BatchDataset
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
    train_dataset: TrainDataset = TrainDataset(train)
    train_dataset.define_train_split(train_split)
    train_dataset.define_feature(feature)
    train_dataset: _BatchDataset = train_dataset.get()
    
    #ValidationDataset Instance
    validation_dataset: ValidationDataset = ValidationDataset(valid)
    validation_dataset.define_train_split(train_split)
    validation_dataset.define_feature(feature)
    valid_dataset: _BatchDataset = validation_dataset.get()
    
    # Model Traning
    model_training: ModelTraining = ModelTraining(train_dataset, valid_dataset)
    model_training._set_model()