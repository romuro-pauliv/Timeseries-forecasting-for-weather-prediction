# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         app.model.normalization.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.log import LogConnectInstance
# | typing |-----------------------------------------------------------------------------------------------------------|
import numpy as np
# |--------------------------------------------------------------------------------------------------------------------|

def _normalizeLog() -> None:
    LogConnectInstance.report("CALC", "LOCAL", "info", True, "NORMALIZATION")

def normalize(data: np.array, train_split: int) -> np.array:
    """
    Normalize 
    Args:
        data (DataFrame): pandas dataframe
        train_split (int): Split Index division

    Returns:
        DataFrame: Normalized dataframe
    """
    data_mean: np.array = data[:train_split].mean(axis=0)
    data_std : np.array = data[:train_split].std(axis=0)
    
    _normalizeLog()
    
    return (data - data_mean) / data_std