from typing import Iterable, List, Union
from theng.data.collection import ADataCollection
from theng.data.pathfinder.triggers import Trigger

class TriggerCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Trigger` objects that provides array-like interface to make accessing trigger data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - TriggerCollection[str] => Gets the first Trigger object whose name matches the provided string.
            - TriggerCollection[int] => Returns the Trigger object at the index specified by int.

    Arguments:
        triggers (Union[Iterable, List]): Trigger objects to put in the collection
    """
    
    def __init__(self, *triggers: Union[Iterable, List]):
        super().__init__(*triggers)
        
    def __getitem__(self,  key: Union[int, str]) -> Union[Trigger, List[Trigger]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(attr for attr in self._elements if (attr.name == key if type(attr) == Trigger  else  attr[0].name == attr))