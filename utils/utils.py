from enum import Enum

class Movement:
    # Normal Moves
    FORWARD = "N"
    BACKWARD = "S"
    LEFT = "W"
    RIGHT = "E"
    FORWARD_LEFT = "NW"
    FORWARD_RIGHT = "NE"
    BACKWARD_LEFT = "SW"
    BACKWARD_RIGHT = "SE"

    # Knight Moves
    NNE = "NNE"
    NNW = "NNW"
    NWW = "NWW"
    NEE = "NEE"
    SEE = "SEE"
    SWW = "SWW"
    SSW = "SSW"
    SSE = "SSE"

    @staticmethod
    def calc_movt(x_steps: int, y_steps: int) -> tuple:
        move = None
        steps = 0
        if x_steps == 0:
            if y_steps > 0:
                move = Movement.RIGHT
            elif y_steps < 0:
                move = Movement.LEFT
            steps = abs(y_steps)
        elif y_steps == 0:
            if x_steps > 0:
                move = Movement.FORWARD
            elif x_steps < 0:
                move = Movement.BACKWARD
            steps = abs(x_steps)
        elif abs(x_steps) == abs(y_steps):
            if x_steps > 0 and y_steps > 0:
                move = Movement.FORWARD_RIGHT
            elif x_steps < 0 and y_steps > 0:
                move = Movement.FORWARD_RIGHT
            elif x_steps > 0 and y_steps < 0:
                move = Movement.BACKWARD_RIGHT
            elif x_steps < 0 and y_steps < 0:
                move = Movement.BACKWARD_LEFT
            steps = abs(x_steps)
        else:
            if x_steps == -1 and y_steps == 2:
                move = Movement.NNW
            elif x_steps == 1 and y_steps == 2:
                move = Movement.NNE
            elif x_steps == -1 and y_steps == -2:
                move = Movement.SSW
            elif x_steps == 1 and y_steps == -2:
                move = Movement.SSE
            elif x_steps == -2 and y_steps == 1:
                move = Movement.NWW
            elif x_steps == 2 and y_steps == 1:
                move = Movement.NEE
            elif x_steps == 2 and y_steps == -1:
                move == Movement.SEE
            elif x_steps == -2 and y_steps == -1:
                move = Movement.SWW
            steps = 1
        return (move, steps)
        
class Position:

    MULTIPLIER = 100

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
        Movement.x: int = _x
        Movement.y: int = _y

    def abs_position(self) -> tuple:
        return (Movement.x, Movement.y)
    
    def map_position(self) -> tuple:
        return (Position.x_map[Movement.x], str(Movement.y + 1))
    
    def get_center_pixel(self) -> tuple:
        center_x = (self.x() * Position.MULTIPLIER) + (Position.MULTIPLIER)
        center_y = (self.y() * Position.MULTIPLIER) + (Position.MULTIPLIER)
        return (center_x, center_y)
    
    def x(self) -> int:
        return Movement.x
    
    def y(self) -> int:
        return Movement.y
    
    @staticmethod
    def map_position_index(x: int) -> str:
        return Position.x_map[x]
    
    def __eq__(self, other) -> bool:
        return Movement.x == other.x and Movement.y == other.y

class Color(Enum):
    BLACK = 0
    WHITE = 1
