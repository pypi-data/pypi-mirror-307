from typing import Iterable, List, Union


from theng.data.collection import ADataCollection
from theng.data.pathfinder.rooms.room import Room


class RoomCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Room` objects that provides array-like interface to make accessing Room data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - RoomCollection[str] => Gets the first Room object whose name matches the provided string.
            - RoomCollection[int] => Returns the Room object at the index specified by int.

    Arguments:
        rooms (Union[Iterable, List]): Room objects to put in the collection
    """
    
    def __init__(self, *rooms: Union[Iterable, List]):
        super().__init__(*rooms)
        
    def __getitem__(self, key: Union[int, str]) -> Union[Room, List[Room]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(room for room in self._elements if (room.name == key if type(room) == Room else room[0].name == key))
    