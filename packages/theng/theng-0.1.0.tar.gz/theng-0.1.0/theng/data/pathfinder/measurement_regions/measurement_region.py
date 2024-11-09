from typing import Dict
from theng.data.a_data_object import ADataObject

from theng.data.time_series import TimeSeries


class MeasurementRegion(ADataObject):
    """Represents a single Measurement Region in a Pathfinder simulation
    
    Args:
        name (str): The name of the Measurement Region.
        data (Dict): Raw data from the _measurement-regions.json file for this Region
            
    Attributes:
        name (str): The name of the Measurement Region
        density (TimeSeries[float]): TimeSeries Object that maps the Region's density measurements to Simulation time
        velocity (TimeSeries[float]): TimeSeries Object that maps the Region's velocity measurements to Simulation time
        seek_velocity (TimeSeries[float]): TimeSeries Object that maps the Region's seek_velocity measurements to Simulation time
            (If Seek Velocity output is enabled).
        count (TimeSeries[float]): TimeSeries Object that maps the Region's Occupant count measurements to Simulation time
    """
    
    def __init__(self, *, name: str, data: Dict) -> None:
        super().__init__()
        self.name = name
        self._data = data
        self.density: TimeSeries[float] = TimeSeries(time=[], values=[])
        self.velocity: TimeSeries[float] = TimeSeries(time=[], values=[])
        self.seek_velocity: TimeSeries[float] = TimeSeries(time=[], values=[])
        self.count: TimeSeries[int] = TimeSeries(time=[], values=[])
        
        self._load()
        
    def _load(self) -> None:
        self._load_safe_time_series(source_data=self._data, data_key='density', target='density')
        self._load_safe_time_series(source_data=self._data, data_key='velocity', target='velocity')
        self._load_safe_time_series(source_data=self._data, data_key='seekVelocity', target='seek_velocity')
        self._load_safe_time_series(source_data=self._data, data_key='count', target='count', data_type=int)
