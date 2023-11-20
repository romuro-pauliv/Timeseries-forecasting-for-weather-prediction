# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      app.resources.extract_data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data import DATAINFO

from connections.log import LogConnectInstance

from zipfile import ZipFile
import pandas as pd
import keras

from pandas.core.frame import DataFrame
# |--------------------------------------------------------------------------------------------------------------------|


class ExtractDataLog:
    @staticmethod
    def _get_file(uri: str, path_: str) -> None:
        LogConnectInstance.report("GET", uri, "info", True, f"PATH {path_}")
    
    @staticmethod
    def _read_csv(filename: str) -> None:
        LogConnectInstance.report("READ", "LOCAL", "info", True, f"{filename}")


class ExtractData(object):
    def __init__(self) -> None:
        """
        Initialize ExtractData instance.
        """
        self.data_uri:      str = DATAINFO['DATA_URI']['uri']
        self.zip_filename:  str = DATAINFO['FILENAMES']['filename_zip']
        self.csv_filename:  str = DATAINFO['FILENAMES']['filename_csv']
        
        self._get_file()
        self._extract_zip()
        
    def _get_file(self) -> None:
        """
        Get data from uri using keras
        """
        self.zip_path: str = keras.utils.get_file(origin=self.data_uri, fname=self.zip_filename)
        ExtractDataLog._get_file(self.data_uri, self.zip_path)
        
    def _extract_zip(self) -> None:
        """
        Extract data using ZipFile
        """
        self.zip_file: ZipFile = ZipFile(self.zip_path)
        self.zip_file.extractall()
    
    def read_csv(self) -> DataFrame:
        """
        Read CSV data and return pandas object
        Returns:
            pandas.core.frame.Dataframe: The csv data
        """
        ExtractDataLog._read_csv(self.csv_filename)
        return pd.read_csv(self.csv_filename)