# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              app.resources.data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data_provider import INIConfig, JsonReader

import configparser
# |--------------------------------------------------------------------------------------------------------------------|

JSON: JsonReader    = JsonReader("app/json")
INI: INIConfig      = INIConfig("app/config")

# | .INI FILES |
INI.load_config()
SERVICESROUTES:         configparser    = INI.config_files['SERVICESROUTES']
DATABASE:               configparser    = INI.config_files['DATABASE']
WHOAMI:                 configparser    = INI.config_files['WHOAMI']

# | JSON |
