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


import statistics
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


class RawHist2DLog:
    @staticmethod
    def _define_fig() -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True, "HIST2D")
    
    @staticmethod
    def _define_var(x_var: str, y_var: str) -> None:
        LogConnectInstance.report("SET", "LOCAL", "info", True, f"X[{x_var}] - Y[{y_var}]")
    
    @staticmethod
    def _show() -> None:
        LogConnectInstance.report("SHOW", "LOCAL", "info", True, "SHOW PLT")


class CorrelationLog:
    @staticmethod
    def _define_fig() -> None:
        LogConnectInstance.report("MAKE", "LOCAL", "info", True, "HEATMAP")
    
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
        plt.clf()


class RawHist2D(object):
    def __init__(self, titles:          list[str] = titles,
                       feature_keys:    list[str] = feature_keys,
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
        self.date_time_key:     list[str]   = date_time_key
        
        self.bins:              tuple[int, int] = (100, 100)
        
    def define_data(self, data: DataFrame) -> None:
        """
        Set data to plot all graphs
        Args:
            data (DataFrame): Pandas dataframe
        """
        self.data: DataFrame = data
    
    def set_variables(self, x_var: int, y_var: int) -> None:
        """
        Set variables based on graph.resources.variables_names.py [feature_keys]
        Args:
            x_var (int): Variable index on feature_key
            y_var (int): Variable index on feature_key
        """
        self.x_var: Series = self.data[self.features_keys[x_var]]
        self.y_var: Series = self.data[self.features_keys[y_var]]

        self.x_var_index: int = x_var
        self.y_var_index: int = y_var
        
        RawHist2DLog._define_var(self.features_keys[x_var], self.features_keys[y_var])
    
    def _make_hist2d(self) -> None:
        """
        Make Hist 2d
        """
        plt.hist2d(self.x_var, self.y_var, bins=self.bins)
        RawHist2DLog._define_fig()
    
    def _set_hist2d_config(self) -> None:
        """
        Set x and y labels and graph title
        """
        plt.title(f"{self.titles[self.x_var_index]} x {self.titles[self.y_var_index]}")
        
        plt.xlabel(f"{self.titles[self.x_var_index]} [{self.features_keys[self.x_var_index]}]")
        plt.ylabel(f"{self.titles[self.y_var_index]} [{self.features_keys[self.y_var_index]}]")
        
    def set_xy_lim(self, x_lim: tuple[float, float], y_lim: tuple[float, float]) -> None:
        """
        define the threshold to x, y variables
        Args:
            x_lim (tuple[float, float]): (min, max) threshold
            y_lim (tuple[float, float]): (min, max) threshold
        """
        plt.xlim(x_lim)
        plt.ylim(y_lim)
            
    def show(self) -> None:
        self._make_hist2d()
        self._set_hist2d_config()
        # self.set_xy_lim((250, 310), (0, 100))
        
        RawHist2DLog._show()
        plt.show()
        plt.clf()


class Correlation(object):
    def __init__(self) -> None:
        """
        Initialize Correlation Instance.
        """
        self.fontsize:  int = 14
        self.rotation:  int = 90
        self.labelsize: int = 14
        
        self.title:    str = "Feature Correlation Heatmap"
    
    def define_data(self, data: DataFrame) -> None:
        """
        Set data to plot all graphs
        Args:
            data (DataFrame): Pandas dataframe
        """
        self.data: DataFrame = data
    
    def show_heatmap(self) -> None:
        """
        Show heatmap correlation
        """
        self.data: DataFrame = self.data.drop(columns=self.data.columns[0])
        plt.matshow(self.data.corr())
        plt.xticks(range(self.data.shape[1]), self.data.columns, fontsize=self.fontsize, rotation=self.rotation)
        plt.gca().xaxis.tick_bottom()
        plt.yticks(range(self.data.shape[1]), self.data.columns, fontsize=self.fontsize)
        
        CorrelationLog._define_fig()
        
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=self.labelsize)
        plt.title(self.title, fontsize=self.fontsize)
        
        
        CorrelationLog._show()
        plt.show()
        plt.clf()