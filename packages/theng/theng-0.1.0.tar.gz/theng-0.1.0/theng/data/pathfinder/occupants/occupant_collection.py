from typing import Iterable, List, Optional, Union
from theng.data.collection import ADataCollection
from theng.data.pathfinder.occupants.occupant import Occupant


class OccupantCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Occupant` objects that provides array-like interface to make accessing Occupant data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - OccupantCollection[str] => Gets the first Occupant object whose name matches the provided string.
            - OccupantCollection[int] => Returns the Occupant object at the index specified by int.

    Arguments:
        occs (Union[Iterable, List]): Occupant objects to put in the collection
    """
    
    def __init__(self, *occs: Union[Iterable, List]):
        super().__init__(*occs)
        
    def __getitem__(self,  key: Union[int, str]) -> Union[Occupant, List[Occupant]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(occ for occ in self._elements if (occ.name == key))
        
    def get_by_id(self, id: int) -> Optional[Occupant]:
        """Search for and return the Occupant whose id attribute matches `id`

        Args:
            id (int): The id to search for
        """
        return next(occ for occ in self._elements if (occ.id == id))