from typing import Dict, List, Union
from theng.data.a_data_object import ADataObject

class Behavior(ADataObject):
    """Represents a single behavior in a Pathfinder simulation.

    Args:
        name (str): The full tree name of the behavior
        data (Dict): Raw data dict for the behavior from the _summary data file.
                    Dictionary should be in the following shape:
                    {
                        "time": {
                            "min": {
                                "occupant": Occupant,
                                "distance": float  
                            },
                            "max": {
                                "occupant": Occupant,
                                "distance": float       
                            },
                            "average": float,
                            "count": int,
                            "stdDev": float
                        }
                        "distance": {
                            "min": {
                                "occupant": Occupant,
                                "distance": float  
                            },
                            "max": {
                                "occupant": Occupant,
                                "distance": float       
                            },
                            "average": float,
                            "count": int,
                            "stdDev": float
                        }
                    }
        
    Attributes:
        name (str): The name of the behavior
        movement_distances (dict): Movement Distance data for this behavior
        completion_times (dict): Completion Time data for this behavior
        count (int): Number of Occupants that used this behavior
    """
    
    def __init__(self, *, name: str, data: Dict):
        super().__init__()
        self.name = name
        self._data = data
        
        self.movement_distances: dict = {}
        self.completion_times: dict = {}
        self.count: int = 0
        
        self._load()
        
    def _load(self) -> None:
        self.count = self._data["time"]["count"]
        self.completion_times = {
            "min": self._data["time"]["min"],
            "max": self._data["time"]["max"],
            "average": self._data["time"]["average"],
            "stdDev": self._data["time"]["stdDev"]
        }
        self.movement_distances = {
            "min": self._data["distance"]["min"],
            "max": self._data["distance"]["max"],
            "average": self._data["distance"]["average"],
            "stdDev": self._data["distance"]["stdDev"]
        }