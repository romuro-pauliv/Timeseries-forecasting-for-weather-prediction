# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.extract_data import ExtractData

from graph.plot_ import RawVisualization, RawHist2D

# | Typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
# |--------------------------------------------------------------------------------------------------------------------|

extract_data: ExtractData = ExtractData()
data: DataFrame = extract_data.read_csv()


# raw_visualization: RawVisualization = RawVisualization()
# raw_visualization.define_data(data)
# raw_visualization.show()

raw_hist_2d: RawHist2D = RawHist2D()
raw_hist_2d.define_data(data)
raw_hist_2d.set_variables(0, 1)
raw_hist_2d.show()