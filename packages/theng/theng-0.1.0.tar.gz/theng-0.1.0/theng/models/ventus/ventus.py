from theng.models import Model

class VentusModel(Model):
    
    def __init__(self, results_file_name: str):
        """Class representing a single Ventus model file"""
        super().__init__(results_file_name, ".ventus")