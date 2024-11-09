class Point():
    """Generic representation of a 3D Point.
    
    Args:
        x (float): X component of the point
        y (float): y component of the point
        z (float): z component of the point
        
    Attributes:
        x (float): X component of the point
        y (float): Y component of the point
        z (float): Z component of the point
    """
    
    def __init__(self, x: float = float('inf'), y: float = float('inf'), z: float = float('inf')):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        
    def __str__(self) -> str:
        return f'Point(X={self.x}, Y={self.y}, Z={self.z})'