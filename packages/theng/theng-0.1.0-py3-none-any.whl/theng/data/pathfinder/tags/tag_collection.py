from typing import Iterable, List, Union
from theng.data.collection import ADataCollection
from theng.data.pathfinder.tags.tag import Tag


class TagCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.Tag` objects that provides array-like interface to make accessing Tag data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - TagCollection[str] => Gets the first Tag object whose name matches the provided string.
            - TagCollection[int] => Returns the Tag object at the index specified by int.

    Arguments:
        tags (Union[Iterable, List]): Tag objects to put in the collection
    """
    
    def __init__(self, *tags: Union[Iterable, List]):
        super().__init__(*tags)
        
    def __getitem__(self, key: Union[int, str]) -> Union[Tag, List[Tag]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(tag for tag in self._elements if (tag.name == key if type(tag) == Tag else tag[0].name == key))