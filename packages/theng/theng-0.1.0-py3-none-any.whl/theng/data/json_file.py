import os, json

from theng.data.data_file import DataFile

class JSONFile(DataFile):
    
    def __init__(self, filepath: str):
        """Class for reading JSON data files
        
        :invar filepath: The path to the JSON file
        :invar data: The data loaded from the JSON file
        """
        super().__init__(filepath)
        if os.path.splitext(filepath)[-1] != ".json":
            raise ValueError("JSONFile was created with a non-JSON filepath.")
        
        with open(filepath,  'r') as f:
            self.data = json.load(f) 