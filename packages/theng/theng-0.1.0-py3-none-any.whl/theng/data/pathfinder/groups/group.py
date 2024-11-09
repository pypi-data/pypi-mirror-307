from typing import Dict, List, Set, Union
from theng.data.a_data_object import ADataObject

from theng.data.time_series import TimeSeries


class Group(ADataObject):
    """Represents a single Group in a Pathfinder simulation
    
    Args:
        group_id (str): The group ID. Must be numeric. (The key in the _groups.json file)
        data (Dict): The data contained under the group ID in the _groups.json file
            
    Attributes:
        id (int): The group ID. Defaults to int(group_id)
        name (str): The name given to this group. Present if this group is predefined before the simulation.
        template (str): The name of the template use to generate this group. Present if this group is generated during the simulation.
        members (List[int]): List of IDs of all historical members of this group.
        member_history (TimeSeries[List[int]]): TimeSeries object storing membership information of this group over the Simulation
    """
    
    def __init__(self, *, group_id: str, data: Dict) -> None:
        super().__init__()
        self.id: int = int(group_id)
        self._data: Dict = data
        
        self.name: str = ""
        self.template: str = ""
        self.members: Union[List, Set] = []
        self.member_history: TimeSeries[List[int]] = TimeSeries(time=[], values=[])
        
        self._load()
        
    def _load(self) -> None:
        self._load_safe(source_data=self._data, data_key='name', target='name')
        self._load_safe(source_data=self._data, data_key='template', target='template')
        
        try:
            self._load_safe_time_series(source_data=self._data, data_key='members', target='member_history')
            for step in self.member_history.values:
                self.members += step
            self.members = set(self.members)
        except:
            pass