from typing import Dict
from theng.data.a_data_object import ADataObject

from theng.data.time_series import TimeSeries


class Trigger(ADataObject):
    """Object representing an Trigger in the Simulation

    Args:
        name (str): The name specified in Pathfinder for this Trigger
        data (dict): Raw data from the _triggers.json file for this Trigger
        
    Attributes:
        name (str): See the `name` argument
        usage (TimeSeries[int]): TimeSeries object that maps the Triggers usage to Simulation Time
        _data (dict): Dictionary storing the raw data from the _triggers.json file
    """
    
    def __init__(self, *, name: str, data: Dict):
        super().__init__()
        self.name: str = name
        self._data: Dict = data
        
        self.usage: TimeSeries[int] = TimeSeries(time=[], values=[])
        
        self._load()
        
    def _load(self) -> None:
        self.usage = TimeSeries(time=[_ for _ in self._data.keys()], values=[int(_) for _ in self._data.values()])