# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.extract_data import ExtractData

from graph.plot_ import RawVisualization

# | Typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
# |--------------------------------------------------------------------------------------------------------------------|

extract_data: ExtractData = ExtractData()
data: DataFrame = extract_data.read_csv()


raw_visualization: RawVisualization = RawVisualization()
raw_visualization.define_data(data)
raw_visualization.show()