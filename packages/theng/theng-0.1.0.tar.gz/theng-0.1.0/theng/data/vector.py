class Vector():
    """Generic representation of a math Vector.
    
    Args:
        x (float): X component of the vector
        y (float): y component of the vector
        z (float): z component of the vector
        magnitude (float): Overall magnitude of the vector
        
    Attributes:
        x (float): X component of the vector
        y (float): Y component of the vector
        z (float): Z component of the vector
        magnitude (float): Overall magnitude of the vectory
    """
    #TODO Refactor magnitude to calculate the magnitude rather than displaying an assigned value.
    
    def __init__(self, x: float = float('inf'), y: float = float('inf'), z: float = float('inf'), magnitude: float = float('inf')):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.magnitude: float = magnitude
        
    def __str__(self) -> str:
        return f'Vector(X={self.x}, Y={self.y}, Z={self.z}, magnitude={self.magnitude})'