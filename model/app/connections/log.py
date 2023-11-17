# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             app.connections.log.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data import WHOAMI, SERVICESROUTES

from connections.services import Connect
from log.local_log import LocalLog

from threads.executable import Threads

from colorama import Fore, Style
from typing import Union

import datetime
import requests
# |--------------------------------------------------------------------------------------------------------------------|

threads: Threads = Threads()

class TerminalLog(object):
    def log_print(self, json_extra: dict[str, dict[str, str]],
                  http_method: str,
                  service_route: str,
                  success: bool,
                  comments: Union[str, None] = None) -> None:
        """
        Display system debug on the run terminal.
        Args:
            json_extra (dict[str, dict[str, str]]): json containing the microservice and clientip
            http_method (str): GET, POST, PUT, DELETE, etc.
            service_route (str): Connection route
            success (bool): Whether the function performed was successful or not
            comments (Union[str, None], optional): Comments if necessary
        """
        
        date: str = f"{Fore.LIGHTYELLOW_EX} {str(datetime.datetime.now())} {Style.RESET_ALL}"
    
        microservice: str = json_extra['extra']['microservice']
        clientip: str = json_extra['extra']['clientip']    
        ami: str = f"{Fore.CYAN}{microservice}{Fore.WHITE} <> {Fore.WHITE}{clientip}{Style.RESET_ALL}"
        
        status: str = f"{Fore.LIGHTMAGENTA_EX}[{http_method}] {Fore.WHITE}{service_route}"
        status_success: str = " [Success]" if success else " [Failed]"
        status += f"{Fore.GREEN if success else Fore.RED}{status_success}{Style.RESET_ALL}"
        
        terminal_log: str = f"{date} | {ami} | {status} "
        
        if comments != None:
            terminal_log += f"{Fore.LIGHTYELLOW_EX}{comments}{Style.RESET_ALL}"
        
        threads.start_thread(print, terminal_log)

class BuildLogJson(object):
    def build_json(self) -> dict[str, Union[str, dict]]:
        """
        Builds a base json with its own process information and the customer's chat_id
        Args:
            chat_id (str): ID of the conversation with the client
        Returns:
            dict[str, Union[str, dict]]: Incomplete JSON payload for the [auto] or [commented] build_json
        """
        return {
            "extra": {
                "microservice": WHOAMI['whoami']['NAME'],
                "clientip": str(WHOAMI['whoami']['HOST'] + ":" + WHOAMI['whoami']['PORT']),
            }
        }

    def log_json(
        self, http_method: str,
              service_route: str,
              success: bool,
              comments: Union[str, None] = None) -> dict[str, Union[str, dict]]:
        """
        Build the JSON payload for the log report.
        Args:
            http_method (str): HTTP method used for communication with the specified service
            service_route (str): Service that the communication was made
            chat_id (str): ID of the conversation with the client
            success (bool): Whether it was successful or not
        Returns:
            dict[str, Union[str, dict]]: JSON payload for the log report.
        """
        json_data: dict[str, Union[str, dict]] = self.build_json()
        
        success_string: str = "Success" if success == True else "Failed"
        json_data["report"] = f"{success_string} on {http_method.upper()} in {service_route.lower()}"
        if comments != None:
            json_data["report"] += f" - {comments}"
        
        TerminalLog().log_print(json_data, http_method, service_route, success, comments)
        return json_data


class LogConnect(Connect, BuildLogJson, LocalLog):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the LogConnect instance.
        """
        self.HOST: str              = str(SERVICESROUTES['LOG']['HOST'])
        self.PORT: str              = str(SERVICESROUTES['LOG']['PORT'])
        self.ROUTE_PARAMETER: str   = str(SERVICESROUTES['LOG.log']['log'])
        
        super().__init__(self.HOST, self.PORT)
        
    def report(
        self, http_method: str, service_route: str,
        log_level: str, success: bool, comments: Union[str, None] = None) -> None:
        """
        Post a report to the log service.
        Args:
            http_method (str): HTTP method used for communication with the specified service
            service_route (str): Service that the communication was made
            log_level (str): Log level ["debug", "info", "warning", "error", "critical"].
            success (bool): Whether it was successful or not
        """
        
        self.set_endpoint(f"{self.ROUTE_PARAMETER}{SERVICESROUTES['LOG.log.endpoints'][log_level]}")
        
        def exec_(http_method: str, service_route: str, success: bool, comments: str) -> None:
            """
            Generated function to be executed in a separate thread
            """
            json: dict[str, str] = self.log_json(http_method, service_route, success, comments)
            response: Union[requests.models.Response, tuple[str, str]] = self.post(json)

            if not isinstance(response, requests.models.Response):
                self.save(json)
        
        threads.start_thread(exec_, http_method, service_route, success, comments)


LogConnectInstance: LogConnect = LogConnect()