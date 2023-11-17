# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     app.resources.data_provider.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import Path, PosixPath
from typing import Any

import configparser
import json
# |--------------------------------------------------------------------------------------------------------------------|

class INIConfig(object):
    def __init__(self, *directory: str) -> None:
        """
        Initialize INIConfig instance.
        """
        self.directory: PosixPath = Path(*directory, "paths.ini")
        
        self.config_paths: configparser.ConfigParser = configparser.ConfigParser()
        self.config_paths.read(self.directory)

        self.config_files: dict[str, configparser.ConfigParser] = {}
        
    def ini(self, ini_file: str) -> configparser.ConfigParser:
        """
        Read .ini files and append configparser.ConsigParser in a dict
        Args:
            ini_file (str): .ini filename in paths.ini section

        Returns:
            configparser.ConfigParser: Istance that content data
        """
        path_str: PosixPath = Path(self.config_paths['PATHS']['master'], self.config_paths[ini_file]['path'])
        config: configparser.ConfigParser = configparser.ConfigParser()
        config.read(path_str)
        return config
    
    def load_config(self) -> None:
        """
        Loads all .ini files to save loading time during scripting 
        """
        for section in self.config_paths.sections():
            if section != "PATHS":
                self.config_files[section] = self.ini(section)
    
    def get(self, ini: str, section: str, key: str) -> str:
        """
        Get data from .ini file
        Args:
            ini (str): .ini filename in paths.ini section
            section (str): section in .ini file
            key (str): key in section from .ini file

        Returns:
            str: data from .ini file
        """
        return self.config_files[ini][section][key]


class JsonReader(object):
    def __init__(self, *directory: str) -> None:
        """
        Initialize a JsonReaded instance and set directory
        """
        self.directory: tuple[str] = directory
    
    def read_json(self, path_: PosixPath) -> dict[str, Any]:
        """
        Read a .json file
        Args:
            path_ (PosixPath): file path

        Returns:
            dict[str, Any]: json data in dict format
        """

        with open(path_, "r+") as file:
            data: dict[str, Any] = json.load(file)
            file.close()
        
        return data
    
    def file_data(self, filename: str) -> dict[str, Any]:
        """
        Retrieve the JSON data from a file
        Args:
            filename (str): The name of the file to read

        Returns:
            dict[str, Any]: The JSON data loaded from the file
        """
        
        directory_file: PosixPath = Path(*self.directory, filename)
        return self.read_json(directory_file)