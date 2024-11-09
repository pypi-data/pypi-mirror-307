from typing import Iterable, List, Union


from theng.data.collection import ADataCollection
from theng.data.pathfinder.behaviors.behavior import Behavior


class BehaviorCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Behavior` objects that provides array-like interface to make accessing Behavior data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - BehaviorCollection[str] => Gets the first Behavior object whose name matches the provided string.
            - BehaviorCollection[int] => Returns the Behavior object at the index specified by int.

    Arguments:
        behaviors (Union[Iterable, List]): Behavior objects to put in the collection
    """
    
    def __init__(self, *behaviors: Union[Iterable, List]):
        super().__init__(*behaviors)
        
    def __getitem__(self, key: Union[int, str]) -> Union[Behavior, List[Behavior]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(behavior for behavior in self._elements if (behavior.name == key if type(behavior) == Behavior else behavior[0].name == key))
    