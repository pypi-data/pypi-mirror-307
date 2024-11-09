from typing import Dict, List
from theng.data.a_data_object import ADataObject
from theng.data.pathfinder.profiles import ProfileCollection, Profile
from theng.data.pathfinder.behaviors import BehaviorCollection, Behavior

class Summary(ADataObject):
    """Placeholder for Simulation Summary data.

    Args:
        data (Data): data
        
    Attributes:
        cpu_time (float):
        startup_time (float):
        components_all (int):
        simulation (str):
        version (str):
        mode (str):
        triangles (int):
        total_occupants (int):
        components_door (int):
        profiles (ProfileCollection):
        behaviors (BehaviorCollection):
        completion_times (dict):
        movement_distances (dict):
        _completion_times_profile (dict):
        _completion_times_behavior (dict):
        _completion_times_all (dict):
        _movement_distances_profile (dict):
        _movement_distances_behavior (dict):
        _movement_distances_all (dict):
        _room_usage (List):
        _door_flow_rates (List):
    """
    
    def __init__(self, parent, data: Dict) -> None:
        super().__init__(parent=parent)
        self._data = data
        
        self.cpu_time: float = float('inf')
        self.startup_time: float = float('inf')
        self.components_all: int = 0
        self.simulation: str = ""
        self.version: str = ""
        self.mode: str = ""
        self.triangles: int = 0
        self.total_occupants: int = 0
        self.components_doors: int = 0
        self.profiles = ProfileCollection([])
        self.behaviors = BehaviorCollection([])
        self.completion_times: dict = {}
        self.movement_distances: dict = {}
        
        self._completion_times_profile: List = []
        self._completion_times_behavior: List = []
        self._completion_times_all: dict = {}
        self._movement_distance_profile: List = []
        self._movement_distances_behavior: List = []
        self._movement_distances_all: dict = {}
        
        self._room_usage: List = []
        self._door_flow_rates: List = []
        
        self._load()
    
    def _load(self) -> None:
        self._load_safe(source_data=self._data, data_key="cpu_time", target="cpu_time")
        self._load_safe(source_data=self._data, data_key="startup_time", target="startup_time")
        self._load_safe(source_data=self._data, data_key="components_all", target="components_all", data_type=int)
        self._load_safe(source_data=self._data, data_key="simulation", target="simulation")
        self._load_safe(source_data=self._data, data_key="version", target="version")
        self._load_safe(source_data=self._data, data_key="mode", target="mode")
        self._load_safe(source_data=self._data, data_key="triangles", target="triangles")
        self._load_safe(source_data=self._data, data_key="total_occupants", target="total_occupants")
        self._load_safe(source_data=self._data, data_key="components_doors", target="components_doors")
        self._load_safe(source_data=self._data, data_key="completion_times_all", target="_completion_times_all")
        self._load_safe(source_data=self._data, data_key="completion_times_profile", target="_completion_times_profile")
        self._load_safe(source_data=self._data, data_key="completion_times_behavior", target="_completion_times_behavior")
        self._load_safe(source_data=self._data, data_key="movement_distances_all", target="_movement_distances_all")
        self._load_safe(source_data=self._data, data_key="movement_distance_profile", target="_movement_distance_profile")
        self._load_safe(source_data=self._data, data_key="movement_distances_behavior", target="_movement_distances_behavior")
        self._load_safe(source_data=self._data, data_key="room_usage", target="_room_usage")
        self._load_safe(source_data=self._data, data_key="door_flow_rates", target="_door_flow_rates")
        
        self._load_completion_times()
        self._load_movement_distances()
        self._load_profiles()
        self._load_behaviors()
        self._load_room_usage()
        self._load_door_flow_rates()
        
        
    def _load_profiles(self) -> None:
        profile_data: dict[str, dict] = {}
        for entry in self._movement_distance_profile:
            profile_data[entry["profile"]] = {}
            profile_data[entry["profile"]]["distance"] = {
                "min": {
                    "occupant": self.parent.occupants[entry["min"]["name"]],
                    "distance": float(entry["min"]["distance"])   
                },
                "max": {
                    "occupant": self.parent.occupants[entry["max"]["name"]],
                    "distance": float(entry["max"]["distance"])       
                },
                "average": float(entry["avg"]),
                "count": int(entry["count"]),
                "stdDev": float(entry["stdDev"])
        }
            
        for entry in self._completion_times_profile:
            profile_data[entry["profile"]]["time"] = {
                "min": {
                    "occupant": self.parent.occupants[entry["min"]["name"]],
                    "time": float(entry["min"]["time"])   
                },
                "max": {
                    "occupant": self.parent.occupants[entry["max"]["name"]],
                    "time": float(entry["max"]["time"])       
                },
                "average": float(entry["avg"]),
                "count": int(entry["count"]),
                "stdDev": float(entry["stdDev"])
            }
            
        profiles: List[Profile] = [Profile(name=name, data=data) for name, data in profile_data.items()]
        self.profiles = ProfileCollection(profiles)
                
    def _load_behaviors(self) -> None:
        behavior_data: dict[str, dict] = {}
        for entry in self._movement_distances_behavior:
            behavior_data[entry["behavior"]] = {}
            behavior_data[entry["behavior"]]["distance"] = {
                "min": {
                    "occupant": self.parent.occupants[entry["min"]["name"]],
                    "distance": float(entry["min"]["distance"])   
                },
                "max": {
                    "occupant": self.parent.occupants[entry["max"]["name"]],
                    "distance": float(entry["max"]["distance"])       
                },
                "average": float(entry["avg"]),
                "count": int(entry["count"]),
                "stdDev": float(entry["stdDev"])
        }
            
        for entry in self._completion_times_behavior:
            behavior_data[entry["behavior"]]["time"] = {
                "min": {
                    "occupant": self.parent.occupants[entry["min"]["name"]],
                    "time": float(entry["min"]["time"])   
                },
                "max": {
                    "occupant": self.parent.occupants[entry["max"]["name"]],
                    "time": float(entry["max"]["time"])       
                },
                "average": float(entry["avg"]),
                "count": int(entry["count"]),
                "stdDev": float(entry["stdDev"])
            }
            
        behaviors: List[Behavior] = [Behavior(name=name, data=data) for name, data in behavior_data.items()]
        self.behaviors = BehaviorCollection(behaviors)
                
    def _load_completion_times(self) -> None:
        if self._data:
            self.completion_times = {
                "min": {
                    "occupant": self.parent.occupants[self._completion_times_all["min"]["name"]],
                    "time": float(self._completion_times_all["min"]["time"])   
                },
                "max": {
                    "occupant": self.parent.occupants[self._completion_times_all["max"]["name"]],
                    "time": float(self._completion_times_all["max"]["time"])       
                },
                "average": float(self._completion_times_all["average"]),
                "stdDev": float(self._completion_times_all["stdDev"])
            }
        
    def _load_movement_distances(self) -> None:
        if self._data:
            self.movement_distances = {
                "min": {
                    "occupant": self.parent.occupants[self._movement_distances_all["min"]["name"]],
                    "distance": float(self._movement_distances_all["min"]["distance"])   
                },
                "max": {
                    "occupant": self.parent.occupants[self._movement_distances_all["max"]["name"]],
                    "distance": float(self._movement_distances_all["max"]["distance"])       
                },
                "average": float(self._movement_distances_all["average"]),
                "stdDev": float(self._movement_distances_all["stdDev"])
            }
        
        
    """
    Loads data from the Summary file in to the Room objects for the relevant Rooms
    """
    def _load_room_usage(self) -> None:
        for room_entry in self._room_usage:
            name = room_entry["room"]
            total_usage = room_entry["total_use"]
            first_in = float(room_entry["first_in"])
            last_out = float(room_entry["last_out"])
            last_out_name: str = room_entry["last_out_name"].strip()
            
            room = self.parent.rooms[name]
            last_out_occ = None
            if last_out_name != "":
                last_out_occ = self.parent.occupants[last_out_name]
            
            room.total_usage = total_usage
            room.first_in_time = first_in
            room.last_out_time = last_out
            room.last_out_occupant = last_out_occ
                
    """
    Loads data from the Summary file in to the Door objects for the relevant Doors
    """
    def _load_door_flow_rates(self) -> None:
        for door_entry in self._door_flow_rates:
            total_usage = door_entry["total_use"]
            name = door_entry["door"]
            first_in = float(door_entry["first_in"])
            last_out = float(door_entry["last_out"])
            
            flow_avg_raw = door_entry["flow_avg"]
            if flow_avg_raw != "":
                flow_avg = float(flow_avg_raw)
            else:
                flow_avg = 0.0
                
            last_out_name = door_entry["last_out_name"].strip()
            last_out_occ = None
            if last_out_name != "":
                last_out_occ = self.parent.occupants[last_out_name]
                
            door = self.parent.doors[name]
            door.total_usage = total_usage
            door.first_in_time = first_in
            door.last_out_time = last_out
            door.flow_avg = flow_avg
            door.last_out_occupant = last_out_occ                