import re, logging
from typing import List, Optional, Union, Dict
from theng.data.a_data_object import ADataObject

from theng.data.pathfinder.direction import Direction
from theng.data.time_series import TimeSeries

#Guards against circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from theng.data.pathfinder.occupants.occupant import Occupant

class Door(ADataObject):
    """Data class that represents a single door in a Pathfinder Simulation
    
    Args:
        name (str): The complete full name of the Door in the Pathfinder model in the form of "Floor -> group -> Doorname"
        data (Dict[str, Union[List[Union[float, int]], Dict[str, List[Union[float, int]]]]]): The raw data dictionary for the Door
            
    Attributes:
        name (str): The complete full name of the Door in the Pathfinder model. e.g. "Floor -> group -> Doorname"
        shortname (str): The last portion of the name attribute. e.g. "Doorname"
        usage (TimeSeries[int]): TimeSeries usage data for the door throughout the simulation
        width (TimeSeries[float]): TimeSeries width data for the door throughout the simulation
        boundary (TimeSeries[float]): TimeSeries boundary width data for the door throughout the simulation
        queueing_usage (TimeSeries[int]): TimeSeries queueing usage data for the door throughout the simulation
        direction (Direction): Direction.BIDIRECTIONAL if this door is not oneway,  one of the other Direction values if otherwise
        total_usage (int): Total number of Occupants that used this door during the simulation.
                            This value is loaded from the _summary.json file and may not be relevant to every Door entry.
        first_in_time (float): Time when an Occupant first used this door during the simulation.
                            This value is loaded from the _summary.json file and may not be relevant to every Door entry.
        last_out_time (float): Time when an Occupant last used this door during the simulation.
                            This value is loaded from the _summary.json file and may not be relevant to every Door entry.
        flow_avg (float): Average flow rate for this door over the entire simulation
                            This value is loaded from the _summary.json file and may not be relevant to every Door entry.
        last_out_occupant (Union[Occupant, None]): The last Occupant to use this door during the simulation
                            This value is loaded from the _summary.json file and may not be relevant to every Door entry.
    """
    
    def __init__(self, *, name: str, data: Dict[str, Union[List[Union[float, int]], Dict[str, List[Union[float, int]]]]]):
        super().__init__()
        self.name: str = name
        self.shortname: str = name.split("->")[-1]
        self._data: Dict[str, Union[List[Union[float, int]], Dict[str, List[Union[float, int]]]]] = data
        
        self.usage: TimeSeries[int] = TimeSeries(time=[], values=[])
        self.width: TimeSeries[float] = TimeSeries(time=[], values=[])
        self.boundary: TimeSeries[float] = TimeSeries(time=[], values=[])
        self.queueing_usage: TimeSeries[int] = TimeSeries(time=[], values=[])
        self.direction: Direction = Direction.BIDIRECTIONAL
        
        if self.name == "exited" or self.name == "remaining":
            self._load_summary_data()
        else:
            self._load_individual_door_data()
            
        self.total_usage: int = 0
        self.first_in_time: float = float('inf')
        self.last_out_time: float = float('inf')
        self.flow_avg: float = float('inf')
        self.last_out_occupant: Union["Occupant", None] = None
                    
    def _load_summary_data(self):
        """Function to load the "exited" and "remaining" door entries, which have a slightly different data structure"""
        self.usage = TimeSeries(time=[_ for _ in self._data.keys()], values=[int(_) for _ in self._data.values()])
            
    def _load_individual_door_data(self):
        """Load all of the potential fields for an individual door"""
        self._load_safe_time_series(source_data=self._data, data_key="usage", target="usage", data_type=int)
        self._load_safe_time_series(source_data=self._data, data_key="width", target="width")
        self._load_safe_time_series(source_data=self._data, data_key="boundary", target="boundary")
        self._load_safe_time_series(source_data=self._data, data_key="queueingDoorUsage", target="queueing_usage")
        
        direction_identifiers: Optional[Union[re.Match, None]] = re.search(r'\[[-+][XYZ]\]', self.name)
        
        if direction_identifiers != None:
            identifier: str = direction_identifiers.group(0)
            if identifier == Direction.X_POSITIVE:
                self.direction = Direction.X_POSITIVE
            elif identifier == Direction.X_NEGATIVE:
                self.direction = Direction.X_NEGATIVE
            elif identifier == Direction.Y_POSITIVE:
                self.direction = Direction.Y_POSITIVE
            elif identifier == Direction.Y_NEGATIVE:
                self.direction = Direction.Y_NEGATIVE
            elif identifier == Direction.Z_POSITIVE:
                self.direction = Direction.Z_POSITIVE
            elif identifier == Direction.Z_NEGATIVE:
                self.direction = Direction.Z_NEGATIVE