from enum import Enum


class Direction(Enum):
    BIDIRECTIONAL = None
    Y_POSITIVE = "[+Y]"
    Y_NEGATIVE = "[-Y]"
    X_POSITIVE = "[+X]"
    X_NEGATIVE = "[-X]"
    Z_POSITIVE = "[+Z]"
    Z_NEGATIVE = "[-Z]"
    
    def __str__(self) -> str:
        if self.value == None:
            return "BiDirectional"
        return self.value.replace("[", "").replace("]", "")
    
    def __eq__(self, other):
        if other == None:
            if self.value == None:
                return True
        
        if isinstance(other, str): 
            return self.value == other
        
        if isinstance(other, Direction):
            return self is other
        
        return False