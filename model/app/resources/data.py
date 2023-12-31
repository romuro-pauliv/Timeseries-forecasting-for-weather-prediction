# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              app.resources.data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data_provider import INIConfig, JsonReader

import configparser

from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

JSON: JsonReader    = JsonReader("app/json")
INI: INIConfig      = INIConfig("app/config")

# | .INI FILES |
INI.load_config()
SERVICESROUTES:         configparser    = INI.config_files['SERVICESROUTES']
MODELARGS:              configparser    = INI.config_files['MODELARGS']
DATABASE:               configparser    = INI.config_files['DATABASE']
DATAINFO:               configparser    = INI.config_files['DATAINFO']
WHOAMI:                 configparser    = INI.config_files['WHOAMI']

# | JSON |
SELECT_VARIABLES:     dict[str, Any]    = JSON.file_data('select_variables.json')
