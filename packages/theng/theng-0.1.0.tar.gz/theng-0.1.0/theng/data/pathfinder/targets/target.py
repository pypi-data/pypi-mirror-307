from typing import Dict, List, Union
from theng.data.a_data_object import ADataObject

from theng.data.time_series import TimeSeries


class Target(ADataObject):
    """Represents a single Occupant Target in a Pathfinder simulation
    
    Args:
        name (str): The name of the Target.
        data (Dict): Raw data from the _occtargets output file for this Target
            
    Attributes:
        name (str): The name of the Target
        is_in_use (TimeSeries[bool]): TimeSeries representing the usage of this Target over time.
        reservation_ids_history (TimeSeries[int]): TimeSeries representing the IDs of Occupants using this Target over time.
        reservation_name_history (TimeSeries[str]): TimeSeries representing the names of Occupants using this Target over time.
    """
    
    def __init__(self, *, name: str, data: Dict):
        super().__init__()
        self.name: str = name
        self._data: Dict = data
        
        self.is_in_use: TimeSeries[bool] = TimeSeries(time=[], values=[])
        self.reservation_ids_history: TimeSeries[int] = TimeSeries(time=[], values=[])
        self.reservation_names_history: TimeSeries[str] = TimeSeries(time=[], values=[])
        
        self._load()
        
    def _load(self) -> None:
        self._load_safe_time_series(source_data=self._data, data_key='using', target='is_in_use')
        self._load_safe_time_series(source_data=self._data, data_key='reservedById', target='reservation_ids')
        self._load_safe_time_series(source_data=self._data, data_key='reservedBy', target='reservation_names')