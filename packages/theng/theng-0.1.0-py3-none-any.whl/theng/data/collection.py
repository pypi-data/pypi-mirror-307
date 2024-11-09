from typing import Iterable, List, Union


class ADataCollection():
    """Base class for any collection of data"""
    
    def __init__(self, *elements: Union[Iterable, List]):
        if type(*elements) == list:
            self._elements = iter(*elements)
        else:
            self._elements = tuple(*elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __iter__(self):
        return self._elements.__iter__()

    def __len__(self):
        return len(self._elements)

    def __contains__(self, value):
        return value in self._elements

    def __repr__(self):
        return "[" + ",\n".join(str(e) for e in self._elements) + "]"

    def clear_cache(self):
        """Remove all data from the internal cache that has been loaded so far to free memory.
        """
        for element in self._elements:
            element.clear_cache()