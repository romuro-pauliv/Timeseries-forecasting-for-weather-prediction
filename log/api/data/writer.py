# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 api.data.writer.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pathlib import PosixPath, Path
from typing import Union
import datetime
import bz2
import os
# |--------------------------------------------------------------------------------------------------------------------|

class Converter:
    @staticmethod
    def json2str(data: dict[str, str]) -> str:
        """
        Convert json log data in str to write in .log file
        Args:
            data (dict[str, str]): json data log

        Returns:
            str: string data log
        """
        date: datetime.datetime = datetime.datetime.utcnow()
        return f"{date} | {data['extra']['microservice']} | {data['extra']['clientip']} | {data['report']}\n"

    @staticmethod
    def B2MB(size_bytes: float) -> float:
        """
        Convert Bytes to MegaBytes
        Args:
            size_bytes (float): Byte size

        Returns:
            float: MegaBytes size
        """
        return size_bytes / (10**6)

class WriterLog(object):
    def __init__(self) -> None:
        """
        Initalize WriterLog Instance.
        """
        self.log_dir: PosixPath = Path("api/log")
        self.logfile_dir: PosixPath
        
        self.datetime_strftime: str = "%d%m%Y%H%M%S"
        
        self.limit_size: float = 100    # In MegaBytes
        
        self._check_dir()
        self._makelogfile_from_logdir()
        
    def _check_dir(self) -> None:
        """
        Check if the dir exists
        """
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
    
    def _scan_path(self) -> Union[None, str]:
        """
        Scan the exists files in self.log_dir directory. If exists .log file, the self.logfile_dir
        is denominate the same name to the file. If not, return None
        Returns:
            Union[None, str]: None or self.logfile_dir.
        """
        file_list: list[str] = os.listdir(self.log_dir)
        for file in file_list:
            i: tuple[str, str] = file.split(".")
            if i[1] == "log":
                return i[0]
        return None
        
    def _makelogfile_from_logdir(self) -> None:
        """
        Create (or take, see _scan_path) the self.logfile_dir.
        """
        scan_file: Union[None, str] = self._scan_path()
        
        if scan_file is None:
            self.logfile_dir: PosixPath = Path(
                self.log_dir,
                f"{datetime.datetime.utcnow().strftime(self.datetime_strftime)}.log"
            )
        else:
            self.logfile_dir: PosixPath = Path(
                self.log_dir,
                f"{scan_file}.log"
            )
    
    def _make_new_logfile(self) -> None:
        """
        Create a new logfile_dir
        """
        self.logfile_dir: PosixPath = Path(
            self.log_dir,
            f"{datetime.datetime.utcnow().strftime(self.datetime_strftime)}.log"
        )
    
    def _size_controller(self) -> bool:
        """
        Control the filesize of .log file. If the file is bigger than self.limit_size, return False.
        Returns:
            bool: False if bigger than limit. True if is not. 
        """
        size: float = os.path.getsize(self.logfile_dir)
        if Converter.B2MB(size) > self.limit_size:
            return False
        return True
    
    def _compact_bz2(self) -> None:
        """
        Compact in (bz2) the .log file that is bigger than the self.limit_size.
        """
        with open(self.logfile_dir, "rb") as dotlogfile:
            with bz2.open(f"{str(self.logfile_dir).split('.')[0]}.bz2", "wb") as dotbz2file:
                dotbz2file.writelines(dotlogfile)
    
    def _remove_logfile(self) -> None:
        """
        Delete logfile. Use only after _compact_bz2 method.
        """
        os.remove(self.logfile_dir)
            
    
    def writer(self, data: dict[str, str]) -> None:
        """
        Write and run the compact structure to .log files.
        Args:
            data (dict[str, str]): _description_
        """
        with open(self.logfile_dir, "a") as file:
            file.write(Converter.json2str(data))
            
            if self._size_controller() == False:
                self._compact_bz2()
                self._remove_logfile()
                self._make_new_logfile()