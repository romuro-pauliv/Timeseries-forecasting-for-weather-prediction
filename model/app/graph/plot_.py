# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 app.graph.plot_.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.log import LogConnectInstance

import matplotlib.pyplot as plt
from graph.resources.variables_names import titles, feature_keys, colors, date_time_key

# | typing |-----------------------------------------------------------------------------------------------------------|
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from matplotlib.axes import _axes
# |--------------------------------------------------------------------------------------------------------------------|

class RawVisualizationLog:
    @staticmethod
    def _define_fig() -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True, "SUBPLOTS")
    
    @staticmethod
    def _make_subplots(plot_name: str) -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True, f"SUBPLOT [{plot_name}]")
        
    @staticmethod
    def _show() -> None:
        LogConnectInstance.report("SHOW", "LOCAL", "info", True, "SHOW PLT")

class RawVisualization(object):
    def __init__(self, titles:          list[str] = titles,
                       feature_keys:    list[str] = feature_keys,
                       colors:          list[str] = colors,
                       date_time_key:   str       = date_time_key) -> None:
        """
        Initalize RawVisualization Instance.
        Args:
            titles (list[str], optional): List of titles. Defaults to titles.
            feature_keys (list[str], optional): Keys to create each graph. Defaults to feature_keys.
            colors (list[str], optional): Colors to each graph. Defaults to colors.
            date_time_key (str, optional): key name to datetime column. Defaults to date_time_key.
        """
        self.titles:            list[str]   = titles
        self.features_keys:     list[str]   = feature_keys
        self.colors:            list[str]   = colors
        self.date_time_key:     list[str]   = date_time_key

        self.fig_nrow:          int             = 7
        self.fig_ncols:         int             = 2
        self.fig_figsize:       tuple[int, int] = (15, 20)
        self.fig_dpi:           int             = 80
        self.fig_facecolor:     str             = "w"
        self.fig_edgecolor:     str             = "k"
        
    def define_data(self, data: DataFrame) -> None:
        """
        Set data to plot all graphs
        Args:
            data (DataFrame): Pandas dataframe
        """
        self.data: DataFrame = data
    
    def _define_pandas_time_data(self) -> None:
        """
        Define pandas datetime series
        """
        self.pandas_time_data: Series = self.data[self.date_time_key]
    
    def _define_fig(self) -> None:
        """
        Define fig and axes instance.
        """
        self.fig, self.axes = plt.subplots(
            nrows=self.fig_nrow, ncols=self.fig_ncols,
            figsize=self.fig_figsize, dpi=self.fig_dpi,
            facecolor=self.fig_facecolor, edgecolor=self.fig_edgecolor
        )
        RawVisualizationLog._define_fig()
    
    def _make_subplots(self) -> None:
        """
        make subplots
        """
        for i in range(len(self.features_keys)):
            key:            str     = self.features_keys[i]
            c:              str     = self.colors[i % len(colors)]
            t_data:         Series  = self.data[key]
            t_data.index:   Series  = self.pandas_time_data 
            t_data.head()
            
            ax: _axes.Axes = t_data.plot(
                ax=self.axes[i // 2, i % 2],
                color=c,
                title=f"{self.titles[i]} - {key}",
                rot=25
            )
            ax.legend(self.titles[i])
            RawVisualizationLog._make_subplots(self.titles[i])
        plt.tight_layout()
            
    def show(self) -> None:
        """
        Show multiplot graphs
        """
        self._define_pandas_time_data()
        self._define_fig()
        self._make_subplots()
        
        RawVisualizationLog._show()
        plt.show()