from typing import Dict, Union
from theng.data.a_data_object import ADataObject

from theng.data.time_series import TimeSeries

#Guards against circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from theng.data.pathfinder.occupants.occupant import Occupant


class Room(ADataObject):
    """Represents a single room in a Pathfinder simulation.

    Args:
        name (str): The full tree name of the room
        data (Dict): Raw data dict for the room from the _rooms data file.
        
    Attributes:
        name (str): The full tree name of the room
        shortname (str): The last portion of the full tree name of the room.
        usage (TimeSeries[int]): Usage data for this door over time
        total_usage (int): Total number of Occupants that have used this room during the simulation. 
                            This data is loaded from the simulation's _summary.json file and is not applicable to every Room
        first_in_time (float): The time when this Room is first use by an Occupant in the simulation. 
                            This data is loaded from the simulation's _summary.json file and is not applicable to every Room
        last_out_time (float): The time when this Room is last used by an Occupant in the simulation. 
                            This data is loaded from the simulation's _summary.json file and is not applicable to every Room
        last_out_occupant (Union[Occupant, None]): The last Occupant to have used this room in the simulation.
                            This data is loaded from the simulation's _summary.json file and is not applicable to every Room
    """
    
    def __init__(self, *, name: str, data: Dict):
        super().__init__()
        self.name = name
        self.shortname = self.name.split('->')[-1]
        self._data = data
        
        self.usage: TimeSeries[int] = TimeSeries(time=[], values=[])
        self.total_usage: int = float('inf')
        self.first_in_time: float = float("inf")
        self.last_out_time: float = float("inf")
        self.last_out_occupant: Union["Occupant", None] = None
        
        self._load()
        
    def _load(self) -> None:
        self.usage = TimeSeries(time=[_ for _ in self._data.keys()], values=[int(_) for _ in self._data.values()])