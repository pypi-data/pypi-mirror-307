class Integer:
    """A simple integer class with basic operations."""
    
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        self._value = value
    
    @property
    def value(self) -> int:
        return self._value
    
    def add(self, other: 'Integer') -> 'Integer':
        """Add another Integer object."""
        if not isinstance(other, Integer):
            raise TypeError("Can only add Integer objects")
        return Integer(self._value + other.value)
    
    def subtract(self, other: 'Integer') -> 'Integer':
        """Subtract another Integer object."""
        if not isinstance(other, Integer):
            raise TypeError("Can only subtract Integer objects")
        return Integer(self._value - other.value)
    
    def __str__(self) -> str:
        return str(self._value)
    
    def __repr__(self) -> str:
        return f"Integer({self._value})"