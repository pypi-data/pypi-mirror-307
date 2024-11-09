
from abc import ABC
import os, logging, subprocess
from typing import Dict, List, Optional, Union

from theng.data.data_file import DataFile
from theng.data.json_file import JSONFile
from theng.plotting import return_image_plot


class Model(ABC):
    """Abstract class that represents a single simulation.

    Args:
        results_file_name (str): The basename of the results file
        extension (str): The standard extension for the simulator file. Used to construct the simulator file name
        
    Attributes:
        model_name (str): The basename of the simulator model file. None if the file is not detected.
        model_file (str): The full name of the simulator model file (basename + extension). None if the file is not detected.
        _log (logging.Logger): Convenience Logger
        _model_extension (str): See :py:attr:`~extension`
        _results_data_files (dict): Container dictionary for all detected results files
        _results_file_name (str): See :py:attr:`~results_file_name`
    """
    
    def __init__(self, results_file_name: str, extension: str):
        self._log: logging.Logger = logging.getLogger(f'theng.{self.__class__.__name__}')
        self._model_extension: str = extension
        self._results_data_files: Dict = {}
        self._results_file_name: str = results_file_name
        
        self.model_name: Optional[str] = None
        self.model_file: Optional[str] = None
        
        basename: str = os.path.splitext(self._results_file_name)[0]
        model_file: str = basename + self._model_extension
        
        if os.path.exists(model_file):
            self.model_file = model_file
            self.model_name = os.path.splitext(model_file)[0]
        else:
            raise ValueError("Results file is not part of a valid Model")
    
    def get_model_name(self) -> Optional[str]:
        """Get the basename of the simulator file
        
        Returns:
            String basename if model file is valid, None if otherwise
        """
        return self.model_name
    
    def get_model_file(self) -> Optional[str]:
        """Get the full filename of the simulator file
        
        Returns:
            String filename if file is valid, None if otherwise
        """
        return self.model_file
        
    def get_all_results_files(self) -> Dict[str, Dict[str, List[DataFile]]]:
        """Get all results data files for this model"""
        return self._results_data_files
    
    def get_results_json_files(self) -> Dict[str, JSONFile]:
        """Get all results data json files for this model"""
        return self._filter_results_files("json")
    
    def get_results_csv_files(self) -> Dict[str, DataFile]:
        """Get all results data csv files for this model"""
        return self._filter_results_files("csv")
    
    def get_results_txt_files(self) -> Dict[str, DataFile]:
        """Get all results data text files for this model"""
        return self._filter_results_files("txt")
                
    def _filter_results_files(self, extension_type: str) -> Dict[str, List[DataFile]]:
        """Get all detected results files for this model that match the given extension type
        
        Params:
            extension_type (str): The extension to filter by. Should match the type in self._results_data_files
        """
        files: Dict[str, List[DataFile]] = {}
        for descriptive_key, file_type_dict in self._results_data_files.items():
            for file_type, data_files in file_type_dict.items():
                if file_type == extension_type and data_files != None:
                    files[descriptive_key] = data_files
        return files
    
    def _take_screenshot(
        self, 
        results_path: str,
        ssview: Union[str, List[str]], 
        ssname: Union[str, List[str], None] = None, 
        sswidth: int = 800, 
        ssheight: int = 600, 
        sstime: Union[float, int] = 0
    ) -> List[str]:
        if type(ssname) == str:
            ssname = [ssname]
        if type(ssview) == str:
            ssview = [ssview]
        
        results: List[str] = []
        if not ssname:
            for view in ssview:
                name = f'{view}.png'
                command: List[str] = [results_path, '-screenshot', '-ssname', name, '-sswidth', str(sswidth), '-ssheight', str(ssheight), '-ssview', view, '-sstime', str(sstime), self._results_file_name]
                p = subprocess.Popen(command)
                p.wait()
                results.append(os.path.abspath(name))
                
                return_image_plot(view, os.path.dirname(os.path.abspath(self.model_file)) + os.sep + name)
        else:
            for name, view in zip(ssname, ssview):
                filename = f'{name}.png'
                command: List[str] = [results_path, '-screenshot', '-ssname', filename, '-sswidth', str(sswidth), '-ssheight', str(ssheight), '-ssview', view, '-sstime', str(sstime), self._results_file_name]
                p = subprocess.Popen(command)
                p.wait()
                results.append(os.path.abspath(filename))
                
                return_image_plot(name, os.path.dirname(os.path.abspath(self.model_file)) + os.sep + filename)
        
        return results