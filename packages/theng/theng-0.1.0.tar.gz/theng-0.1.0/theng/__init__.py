"""`theng </>`_ is a data processing toolset for common Life Safety simulators and a collection of utilities for displaying processed data in Thunderhead Results.
This toolset is designed for use in the Scripting Engine of the `Thunderhead Results Viewer <https://thunderheadeng.com>`_, however it can also be used in standalone Python scripts.

Attributes:
    log(Optional[logging.Logger]): A preconfigured logger that writes output to the script log file.
    VERSION(str): The version of the installed theng package
"""
import sys

from theng.main import *
from theng.logging import get_theng_logger, _initialize_logger
from theng.args import add_model_paths, suppress_warnings

log: Optional[logging.Logger] = None
if 'sphinx' not in sys.argv[0]:
    _initialize_logger()
    log = get_theng_logger(sys.argv[0])   
    
__all__ = ["get_models", "get_pathfinder_models", "get_pyrosim_models", "get_ventus_models", "get_theng_logger", "add_model_paths", "suppress_warnings"]

VERSION: str = "0.1.0"