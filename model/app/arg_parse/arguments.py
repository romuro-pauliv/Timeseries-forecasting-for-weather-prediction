# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app.arg_parse.arguments.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import argparse
# |--------------------------------------------------------------------------------------------------------------------|

parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Timeseries Forecasting for Weather Prediction")

# Store True |---------------------------------------------------------------------------------------------------------|
parser.add_argument('--graph',
                    action="store_true",
                    help="Show the data graph analysis"
                    )
parser.add_argument('--hist2d',
                    action='store_true',
                    help="Show Hist2D to analysis data [use --hist2dx --hist2dy] to set variables"
                    )
parser.add_argument('--correlation',
                    action='store_true',
                    help='Show correlation heatmap between the all variables')
# |--------------------------------------------------------------------------------------------------------------------|

# Values |-------------------------------------------------------------------------------------------------------------|
parser.add_argument('--hist2dx', type=int, default=0, help="Variable Index from app.graph.resources.variable_names.py")
parser.add_argument('--hist2dy', type=int, default=1, help="Variable Index from app.graph.resources.variable_names.py")
# |--------------------------------------------------------------------------------------------------------------------|

args: argparse.Namespace = parser.parse_args()
