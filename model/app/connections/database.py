# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        app.connections.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.log import LogConnectInstance
from resources.data import DATABASE

from pymongo import MongoClient
from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|


class MongoConnectLog:
    @staticmethod
    def connect(uri: str, event: bool) -> None:
        if event is True:
            LogConnectInstance.report("SOCKET", uri, "info", event)
            return None
        LogConnectInstance.report("SOCKET", uri, "error", event)

    @staticmethod
    def database_list_names(uri: str, event: bool) -> None:
        message: str = "DATABASE LIST NAMES"
        if event is True:
            LogConnectInstance.report("GET", uri, "info", event, message)
            return None
        LogConnectInstance.report("GET", uri, "error", event, message)
    
    @staticmethod
    def collection_list_names(uri: str, event: bool, database: str) -> None:
        message: str = f"COLLECTION LIST NAMES [{database}]"
        if event is True:
            LogConnectInstance.report("GET", uri, 'info', event, message)
            return None
        LogConnectInstance.report("GET", uri, 'error', event, message)
    
    @staticmethod
    def create_collection(uri: str, event: bool, database: str, collection: str) -> None:
        message: str = f"[{collection}] IN [{database}]"
        if event is True:
            LogConnectInstance.report("POST", uri, "info", event, message)
            return None
        LogConnectInstance.report("POST", uri, "error", event, message)
     
    @staticmethod
    def create_index(uri: str, event: bool, database: str, collection: str, key: str) -> None:
        message: str = f"INDEX [{database}][{collection}] - K({key})"
        if event is True:
            LogConnectInstance.report("POST", uri, "info", event, message)
            return None
        LogConnectInstance.report("POST", uri, "error", event, message)
    
    @staticmethod
    def post(uri: str, event: bool, type_: str, log_comment: str, database: str, collection: str) -> None:
        if event is True:
            LogConnectInstance.report("POST", uri, "info", event, f"[{database}][{collection}] {type_} {log_comment}")
            return None
        LogConnectInstance.report("POST", uri, "error", event, f"[{database}][{collection}] {type_} {log_comment}")
    
    @staticmethod
    def get(uri: str, event: bool, database: str, collection: str, query: str) -> None:
        message: str = f"{database}|{collection} - {query}"
        if event is True:
            LogConnectInstance.report("GET", uri, "info", True, message)
            return None
        LogConnectInstance.report("GET", uri, "error", False, query)

  
class MongoConnect(object):
    def __init__(self) -> None:
        """
        Initialize MongoConnect instance.
        
        Initializes a connection to the MongoDB server using the specified 
        HOST and PORT from the DATABASE configuration.
        """
        HOST: str       = DATABASE['mongodb']['HOST']
        PORT: str       = DATABASE['mongodb']['PORT']
        self.uri: str   = f"{HOST}:{PORT}"
        
        self._connect()
        
    def _connect(self) -> None:
        """
        Establishes a connection to the MongoDB server.

        Attempts to connect to the MongoDB server using the URI specified 
        in the instance, and logs the connection event.Exits the program 
        if the connection fails.
        """
        try:
            self.connect: MongoClient = MongoClient(self.uri)
            MongoConnectLog.connect(self.uri, True)
        except Exception:
            MongoConnectLog.connect(self.uri, False)
            exit()
    

    def collection_list_names(self, database: str) -> list[str]:
        """
        Retrieves a list of collection names on the MongoDB server.
        Args:
            database (str): A database name

        Returns:
            list[str]: A list of collection names on the database
        """
        try:
            collection_list_names: list[str] = self.connect[database].list_collection_names()
            MongoConnectLog.collection_list_names(self.uri, True, database)
        except Exception:
            MongoConnectLog.collection_list_names(self.uri, False, database)
        
        return collection_list_names
    
    def create_collection(self, database: str, collection: str) -> None:
        """
        Create a new collection on a specified database
        Args:
            database (str): Database to create a new collection
            collection (str): Collection name
        """
        try:
            self.connect[database].create_collection(collection)
            MongoConnectLog.create_collection(self.uri, True, database, collection)
        except Exception:
            MongoConnectLog.create_collection(self.uri, False, database, collection)
            
    def post(self, database: str, collection: str,
             documents: Union[list[dict[str, Any]], dict[str, Any]],
             log_comment: str,
             show_log: bool) -> None:
        """
        Inserts one or multiple documents into a MongoDB collection.

        Args:
            database (str): The name of the MongoDB database.
            collection (str): The name of the collection within the database.
            documents (Union[list[dict[str, Any]], dict[str, Any]]): A single document or a list of documents to insert.
            log_comment (str): A comment or description to include in the log message.
        """
        if isinstance(documents, dict):
            try:
                self.connect[database][collection].insert_one(documents)
                if show_log is True:
                    MongoConnectLog.post(self.uri, True, "INSERT DOC", log_comment, database, collection)
            except Exception:
                MongoConnectLog.post(self.uri, False, "INSERT DOC", log_comment, database, collection)
                                
        if isinstance(documents, list):
            try:
                self.connect[database][collection].insert_many(documents)
                if show_log is True:
                    MongoConnectLog.post(self.uri, True, f"INSERT {len(documents)} DOCS", log_comment, database, collection)
            except Exception:
                MongoConnectLog.post(self.uri, False, f"INSERT {len(documents)} DOCS", log_comment, database, collection)
        
    def create_index(self, database: str, collection: str, key: str, pymongo_mode: str, unique: bool) -> None:
        """
        Creates an index on a MongoDB collection.

        Args:
            database (str): The name of the MongoDB database.
            collection (str): The name of the collection within the database.
            key (str): The field to create an index on.
            pymongo_mode (str): The pymongo index mode, e.g., ASCENDING, DESCENDING, etc.
            unique (bool): Whether the index should be unique.
        """
        try:
            self.connect[database][collection].create_index([(key, pymongo_mode)], unique=unique)
            MongoConnectLog.create_index(self.uri, True, database, collection, key)
        except Exception:
            MongoConnectLog.create_index(self.uri, False, database, collection, key)
    
    def get(self, database: str, collection: str, query: dict[str, Any]) -> Union[list[dict[str, Any]], None]:
        """
        Get data from MongoDB by query
        Args:
            database (str): The name of the MongoDB database
            collection (str): The name of the collection within the database
            query (dict[str, Any]): Query to find document in the collection

        Returns:
            list[dict[str, Any]]: Document in a list or None
        """
        try:
            data: list[dict[str, Any]] = list(self.connect[database][collection].find(query))
            if isinstance(data, list):
                MongoConnectLog.get(self.uri, True, database, collection, query)
                return data
            else:
                MongoConnectLog.get(self.uri, False, database, collection, query)
                return None
        except Exception:
            MongoConnectLog.get(self.uri, False, database, collection, query)
            return None
    
    def get_one(self, database: str, collection: str, query: dict[str, Any],
                      sort: list[Any]) -> Union[dict[str, Any], None]:
        """
        Get one document from mongoDB by the query
        Args:
            database (str): The name of the MongoDB database
            collection (str): The name of the collection within the database
            query (dict[str, Any]): Query to find document in the collection

        Returns:
            Union[list[dict[str, Any]], None]: Document in a list or None
        """

        try:
            data: dict[str, Any] = self.connect[database][collection].find_one(query, sort=sort)
            if isinstance(data, dict):
                MongoConnectLog.get(self.uri, True, database, collection, query)
                return data
            else:
                MongoConnectLog.get(self.uri, False, database, collection, query)
                return None
        except Exception:
            MongoConnectLog.get(self.uri, False, database, collection, query)
        
        
MongoConnectInstance: MongoConnect = MongoConnect()