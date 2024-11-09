from typing import Iterable, List, Union
from theng.data.collection import ADataCollection
from theng.data.pathfinder.doors import Door

class DoorCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Door` objects that provides array-like interface to make accessing Door data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - DoorCollection[str] => Gets the first Door object whose name matches the provided string.
            - DoorCollection[int] => Returns the Door object at the index specified by int.

    Arguments:
        doors (Union[Iterable, List]): Door objects to put in the collection
    """
    
    def __init__(self, *doors: Union[Iterable, List]):
        super().__init__(*doors)
        
    def __getitem__(self,  key: Union[int, str]) -> Union[Door, List[Door]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(door for door in self._elements if (door.name == key if type(door) == Door  else  door[0].name == door))