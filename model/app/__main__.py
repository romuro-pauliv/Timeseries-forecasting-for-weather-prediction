# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.extract_data import ExtractData

from graph.plot_ import RawVisualization, RawHist2D, Correlation
from arg_parse.arguments import args

# | Typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
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
    