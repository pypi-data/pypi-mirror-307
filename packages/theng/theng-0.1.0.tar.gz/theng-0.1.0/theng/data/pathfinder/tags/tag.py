"""Tag support is preliminary at this point. This currently serves as a data module for Occupants. 
There is hope for more model-level Tag functionality in the future.
"""

from typing import Dict, Optional
from theng.data.a_data_object import ADataObject


class Tag(ADataObject):
    """Represents a single Tag applied to an object in a Pathfinder simulation

    Args:
        name (str): The name of the Tag
        data (Dict): Raw data dict for the tag.
        
    Attributes:
        usage (Optional[float]): The amount of time that this Tag was applied to the relevant Occupant
        last_added(Optional[float]): The last timestep when this Tag was added to the relevant Occupant
        last_removed(Optional[float]): The last timestep when this Tag was removed from the relevant Occupant
    """
    
    def __init__(self, name: str, data: Dict):
        super().__init__()
        self.name = name
        self._data = data
        
        self.usage: Optional[float] = None
        self.last_added: Optional[float] = None
        self.last_removed: Optional[float] = None
        
        self._load()
    
    def _load(self) -> None:
        self._load_safe(source_data=self._data, data_key="usageTime", target="usage")
        self._load_safe(source_data=self._data, data_key="lastAdded", target="last_added")
        self._load_safe(source_data=self._data, data_key="lastRemoved", target="last_removed")