from abc import ABC
from logging import Logger
from typing import Any, Dict
from theng.data.time_series import TimeSeries

from theng.logging import get_theng_logger
from theng.args import get_arguments

class ADataObject(ABC):
    
    def __init__(self, parent: Any = None):
        self.parent = parent
        self._log: Logger = get_theng_logger(str(self.__class__.__name__))
    
    def _load_safe(self, *, source_data: Dict, data_key: str, target: str, e_message: str = None, data_type: Any = None) -> None:
        """Safely load a value from a dictionary in to this class as an attribute with name defined by `target`

        Args:
            source_data (Dict): The data dictionary to load from
            data_key (str): The key in the dictionary to pull the value from
            target (str): The attribute name to set on this class
            e_message (str, optional): A message to warn in the log if the data_key cannot be accessed. Defaults to None.
            data_type (Any): The type to cast any dictionary values to. Defaults to None, which will just load the data as whatever type it already is.
        """
        try:
            val: Any = source_data[data_key]
            if val == "None" or val == "":
                val = None
            if data_type != None and val != None:
                self.__setattr__(target, data_type(val))
            else:
                self.__setattr__(target, val)
        except KeyError:
            if e_message != None and not get_arguments().quiet:
                self._log.warning(e_message)
                
    def _load_safe_time_series(self, *, source_data: Dict, data_key: str, target: str, e_message: str = None, data_type: Any = None) -> None:
        """Safely load a TimeSeries in to this class from a dictionary as an attribute with the name defined by `target`

        Args:
            source_data (Dict): The data dictionary to load from
            data_key (str): The key in the dictionary to pull the values from
            target (str): The attribute name to set on this class
            e_message (str, optional): A message to warn in the log if the data_key cannot be accessed. Defaults to None.
            data_type (Any): The type to cast any dictionary values to. Defaults to None, which will just load the data as whatever type it already is.
        """
        try:
            if data_type != None:
                self.__setattr__(target, TimeSeries(time=[_ for _ in source_data[data_key].keys()], values=[data_type(_) for _ in source_data[data_key].values()]))
            else:
                self.__setattr__(target, TimeSeries(time=[_ for _ in source_data[data_key].keys()], values=[_ for _ in source_data[data_key].values()]))
        except KeyError:
            if e_message != None and not get_arguments().quiet:
                self._log.warning(e_message)