# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               app.log.local_log.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import Path, PosixPath
from typing import Any
import datetime
import os
# |--------------------------------------------------------------------------------------------------------------------|


class BuildLog(object):
    def json2log(self, data: dict[str, Any]) -> str:
        """
        transforms the json built in str to write to .log
        Args:
            data (dict[str, Any]): Complete JSON payload from log_json method

        Returns:
            str: string with the json information
        """
        date: datetime.datetime     = datetime.datetime.utcnow()
        info: dict[str, str]        = data["extra"]
        report: str                 = data["report"]
        return f"{date} | {info['microservice']} | {info['clientip']} | {report}\n"


class LocalLog(BuildLog):
    def __init__(self) -> None:
        """
        Initialize the LocalLog instance.
        """
        super().__init__()
    
    def check_dir(self) -> None:
        """
        Create a log directory in app/log/files
        """
        self.log_directory: PosixPath  = Path("app", "log", "files")
        if not os.path.exists(self.log_directory):
            os.mkdir(self.log_directory)
    
    def save(self, data: dict[str, Any]) -> None:
        """
        create a log directory in app/log/files and create an offline.log file to append logs if the connection to the 
        log service is not established
        Args:
            data (dict[str, Any]): json that would be sent to the log service
        """
        self.check_dir()
        data: str = self.json2log(data)
        self.log_file_path: PosixPath = Path(self.log_directory, "offline.log")
        with open(self.log_file_path, "a") as file:
            file.write(data)