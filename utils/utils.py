class Movement:
    VERTICAL = 0
    HORIZONTAL = 1
    DIAGONAL = 2

    FORWARD = "N"
    BACKWARD = "S"
    LEFT = "W"
    RIGHT = "E"
    FORWARD_LEFT = "NW"
    FORWARD_RIGHT = "NE"
    BACKWARD_LEFT = "SW"
    BACKWARD_RIGHT = "SE"

    MULTIPLE = -1
    SINGULAR = 1

    @staticmethod
    def is_vertical(direction: str) -> bool:
        return direction in [Movement.FORWARD, Movement.BACKWARD]
    
    @staticmethod
    def is_horizontal(direction: str) -> bool:
        return direction in [Movement.LEFT, Movement.RIGHT]
    
    @staticmethod
    def is_diagonal(direction: str) -> bool:
        return direction in [Movement.FORWARD_LEFT, Movement.FORWARD_RIGHT, Movement.BACKWARD_LEFT, Movement.BACKWARD_RIGHT]
    
    @staticmethod
    def is_valid(constraints: list, direction: str) -> bool:
        for constraint in constraints:
            if Movement.is_valid_constraint(constraint, direction):
                return True
        return False
    
    @staticmethod
    def is_valid_constraint(constraint: int, direction: str) -> bool:
        if constraint == Movement.VERTICAL:
            return Movement.is_vertical(direction)
        elif constraint == Movement.HORIZONTAL:
            return Movement.is_horizontal(direction)
        elif constraint == Movement.DIAGONAL:
            return Movement.is_diagonal(direction)
        else:
            return False
        
class Position:

    x_map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H"
    }

    def __init__(self, _x: int, _y: int) -> None:
        self.x: int = _x
        self.y: int = _y

    def abs_position(self) -> tuple:
        return (self.x, self.y)
    
    def map_position(self) -> tuple:
        return (Position.x_map[self.x], str(self.y + 1))
    
    def x(self) -> int:
        return self.x
    
    def y(self) -> int:
        return self.y
    
    @staticmethod
    def map_position_index(x: int) -> str:
        return Position.x_map[x]
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

