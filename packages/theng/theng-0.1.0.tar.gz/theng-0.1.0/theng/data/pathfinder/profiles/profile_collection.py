from typing import Iterable, List, Union


from theng.data.collection import ADataCollection
from theng.data.pathfinder.profiles.profile import Profile


class ProfileCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Profile` objects that provides array-like interface to make accessing Profile data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - ProfileCollection[str] => Gets the first Profile object whose name matches the provided string.
            - ProfileCollection[int] => Returns the Profile object at the index specified by int.

    Arguments:
        profiles (Union[Iterable, List]): Profile objects to put in the collection
    """
    
    def __init__(self, *profiles: Union[Iterable, List]):
        super().__init__(*profiles)
        
    def __getitem__(self, key: Union[int, str]) -> Union[Profile, List[Profile]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(profile for profile in self._elements if (profile.name == key if type(profile) == Profile else profile[0].name == key))
    