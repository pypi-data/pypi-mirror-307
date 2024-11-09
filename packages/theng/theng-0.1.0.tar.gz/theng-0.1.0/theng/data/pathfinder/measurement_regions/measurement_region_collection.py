from typing import Iterable, List, Union
from theng.data.collection import ADataCollection
from theng.data.pathfinder.measurement_regions.measurement_region import MeasurementRegion


class MeasurementRegionCollection(ADataCollection):
    """Collection of :class:`~theng.data.pathfinder.MeasurementRegion` objects that provides array-like interface to make accessing MeasurementRegion data a little easier.
    
    Example:
        Elements in the Collection can be accessed in the following ways:
            - MeasurementRegionCollection[str] => Gets the first MeasurementRegion object whose name matches the provided string.
            - MeasurementRegionCollection[int] => Returns the MeasurementRegion object at the index specified by int.

    Arguments:
        regions (Union[Iterable, List]): MeasurementRegion objects to put in the collection
    """
    
    def __init__(self, *regions: Union[Iterable, List]):
        super().__init__(*regions)
        
    def __getitem__(self,  key: Union[int, str]) -> Union[MeasurementRegion, List[MeasurementRegion]]:
        if type(key) == int:
            return self._elements[key]
        else:
            return next(region for region in self._elements if (region.name == key))