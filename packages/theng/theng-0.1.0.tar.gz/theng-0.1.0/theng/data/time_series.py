from typing import Generic, List, TypeVar, Union, Self

T = TypeVar("T") 

class TimeSeries(Generic[T]):
    """Used to store Time Series based data about a Simulation
    
    Args:
        time (List[float]): Timesteps at which the data was written.
        values (List): A list of data corresponding to the Timesteps
            
    Attributes:
        time (List[float]): Timesteps at which the data was written.
        values (List[T]): A list of data corresponding to the Timesteps
    """
    
    def __init__(self, *, time: List[float], values: List[T]) -> None:
        self.index = 0
        self.time: List[float] = [float(x) for x in time]
        self.values: List[T] = values
        
    def __iter__(self):
        return TimeSeries(time=self.time, values=self.values)
    
    def __next__(self):
        next_obj = None
        while (next_obj is None):
            if self.index >= min(len(self.time), len(self.values)):
                raise StopIteration
            next_obj = [self.time[self.index], self.values[self.index]]
            self.index += 1
        return next_obj
    
    def __getitem__(self, key):
        if key <= len(self.time) and key <= len(self.values):
            return (self.time[key], self.values[key])
        raise IndexError
    
    """Filters the TimeSeries using a minimum and optional maximum time
    
    Args:
        min (float): The minimum time, inclusive, to filter by
        max (Optional[float, None]): The optional maximum time, inclusive, to filter by
        
    Returns:
        A new TimeSeries containing the filtered data.
    """
    def filter_by_time(self, min: float, max: Union[float, None] = None) -> Self:
        filtered_times = []
        filtered_values = []
        for [time, value] in self:
            if time >= min:
                if max == None or time <= max:
                    filtered_times.append(time)
                    filtered_values.append(value)
                    
        return TimeSeries(time=filtered_times, values=filtered_values)
    
    """Filters the TimeSeries using a minimum and optional maximum value
    
    Args:
        min (float): The minimum value, inclusive, to filter by
        max (Optional[float, None]): The optional maximum value, inclusive, to filter by
        
    Returns:
        A new TimeSeries containing the filtered data.
    """
    def filter_by_value(self, min: float, max: Union[float, None] = None) -> Self:
        filtered_times = []
        filtered_values = []
        for [time, value] in self:
            if value >= min:
                if  max == None or value <= max:
                    filtered_times.append(time)
                    filtered_values.append(value)
                    
        return TimeSeries(time=filtered_times, values=filtered_values)