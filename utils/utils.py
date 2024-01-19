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