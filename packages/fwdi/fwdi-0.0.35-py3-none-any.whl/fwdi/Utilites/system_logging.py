import os
from threading import get_ident, current_thread, get_native_id
from enum import Enum
import logging


class TypeLogging(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    NOTSET = 5

logging.basicConfig(filename='__system__.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s | %(name)s | %(levelname)s | %(thread)d | %(message)s')

class SysLogging():
    def __init__(self, filename:str, logging_level=TypeLogging.DEBUG):
        self.__LOG_DIR = 'logs'
        self.__filename = f'{self.__LOG_DIR}/ITSHelper_{filename}.log'

        match(logging_level):
            case TypeLogging.INFO:
                level_log = logging.INFO
            case TypeLogging.DEBUG:
                level_log = logging.DEBUG
            case TypeLogging.WARNING:
                level_log = logging.WARNING
            case TypeLogging.ERROR:
                level_log = logging.ERROR
            case TypeLogging.CRITICAL:
                level_log = logging.CRITICAL
            case TypeLogging.NOTSET:
                level_log = logging.NOTSET
        
        if not os.path.exists(self.__LOG_DIR):
            os.mkdir(self.__LOG_DIR)

        self.__logger = logging.getLogger(self.__filename)
        self.__logger.setLevel(level_log)
        
        formatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s | %(thread)d | %(message)s')
        file_handler = logging.FileHandler(self.__filename)
        file_handler.setLevel(level_log)
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)

    def __call__(self, message:str, type_log:str='INFO', args:any=None):
        message = f"ident={get_ident()}, id={get_native_id()}::{message}"
        match(type_log.upper()):
            case 'INFO':
                self.__logger.info(message)
            case 'DEBUG':
                self.__logger.debug(message)
            case 'WARNING':
                self.__logger.warning(message)
            case 'ERROR':
                self.__logger.error(message)
            case _:
                self.__logger.info(message)