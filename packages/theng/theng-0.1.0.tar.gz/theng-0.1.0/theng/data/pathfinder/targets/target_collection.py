from typing import Iterable, List, Union
from theng.data.collection import ADataCollection
from theng.data.pathfinder.targets import Target

class TargetCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Target` objects that provides array-like interface to make accessing Target data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - TargetCollection[str] => Gets the first Target object whose name matches the provided string.
            - TargetCollection[int] => Returns the Target object at the index specified by int.

    Arguments:
        targets (Union[Iterable, List]): Target objects to put in the collection
    """
    
    def __init__(self, *targets: Union[Iterable, List]):
        super().__init__(*targets)
        
    def __getitem__(self,  key: Union[int, str]) -> Union[Target, List[Target]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(target for target in self._elements if (target.name == key if type(target) == Target  else  target[0].name == target))