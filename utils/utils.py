from enum import Enum
import math

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
    def calc_movt(x_steps: int, y_steps: int, inverse: bool = False) -> tuple:
        inverse_map = {
            Movement.FORWARD: Movement.BACKWARD,
            Movement.BACKWARD: Movement.FORWARD,
            Movement.LEFT: Movement.RIGHT,
            Movement.RIGHT: Movement.LEFT,
            Movement.FORWARD_LEFT: Movement.BACKWARD_RIGHT,
            Movement.FORWARD_RIGHT: Movement.BACKWARD_LEFT,
            Movement.BACKWARD_LEFT: Movement.FORWARD_RIGHT,
            Movement.BACKWARD_RIGHT: Movement.FORWARD_LEFT,
            Movement.NNE: Movement.SSW,
            Movement.NNW: Movement.SSE,
            Movement.NWW: Movement.SEE,
            Movement.NEE: Movement.SWW,
            Movement.SEE: Movement.NWW,
            Movement.SWW: Movement.NEE,
            Movement.SSW: Movement.NNE,
            Movement.SSE: Movement.NNW
        }

        move = None
        steps = 0
        if x_steps == 0:
            if y_steps > 0:
                move = Movement.FORWARD
            elif y_steps < 0:
                move = Movement.BACKWARD
            steps = abs(y_steps)
        elif y_steps == 0:
            if x_steps > 0:
                move = Movement.RIGHT
            elif x_steps < 0:
                move = Movement.LEFT
            steps = abs(x_steps)
        elif abs(x_steps) == abs(y_steps):
            if x_steps > 0 and y_steps > 0:
                move = Movement.FORWARD_RIGHT
            elif x_steps < 0 and y_steps > 0:
                move = Movement.FORWARD_LEFT
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
                move = Movement.SEE
            elif x_steps == -2 and y_steps == -1:
                move = Movement.SWW
            steps = 1

        if inverse:
            if move:
                move = inverse_map[move]
        return (move, steps)
    
    @staticmethod
    def calculate_direction(_from: tuple, _to: tuple, inverse: bool = False) -> tuple:
        x_steps = _to[0] - _from[0]
        y_steps = _to[1] - _from[1]
        return Movement.calc_movt(x_steps, y_steps, inverse)
    
    @staticmethod
    def predict_position(_from: tuple, _direction: str, _steps: int, inverse: bool = False) -> tuple:
        x = _from[0]
        y = _from[1]
        if _direction == Movement.FORWARD:
            if inverse:
                y -= _steps
            else:
                y += _steps
        elif _direction == Movement.BACKWARD:
            if inverse:
                y += _steps
            else:
                y -= _steps
        elif _direction == Movement.LEFT:
            if inverse:
                x += _steps
            else:
                x -= _steps
        elif _direction == Movement.RIGHT:
            if inverse:
                x -= _steps
            else:
                x += _steps
        elif _direction == Movement.FORWARD_LEFT:
            if inverse:
                x += _steps
                y -= _steps
            else:
                x -= _steps
                y += _steps
        elif _direction == Movement.FORWARD_RIGHT:
            if inverse:
                x -= _steps
                y -= _steps
            else:
                x += _steps
                y += _steps
        elif _direction == Movement.BACKWARD_LEFT:
            if inverse:
                x += _steps
                y += _steps
            else:
                x -= _steps
                y -= _steps
        elif _direction == Movement.BACKWARD_RIGHT:
            if inverse:
                x -= _steps
                y += _steps
            else:
                x += _steps
                y -= _steps
        elif _direction == Movement.NNE:
            if inverse:
                x -= 1
                y -= 2
            else:
                x += 1
                y += 2
        elif _direction == Movement.NNW:
            if inverse:
                x += 1
                y -= 2
            else:
                x -= 1
                y += 2
        elif _direction == Movement.NWW:
            if inverse:
                x += 2
                y -= 1
            else:
                x -= 2
                y += 1
        elif _direction == Movement.NEE:
            if inverse:
                x -= 2
                y -= 1
            else:
                x += 2
                y += 1
        elif _direction == Movement.SEE:
            if inverse:
                x -= 2
                y += 1
            else:
                x += 2
                y -= 1
        elif _direction == Movement.SWW:
            if inverse:
                x += 2
                y += 1
            else:
                x -= 2
                y -= 1
        elif _direction == Movement.SSW:
            if inverse:
                x += 1
                y += 2
            else:
                x -= 1
                y -= 2
        elif _direction == Movement.SSE:
            if inverse:
                x -= 1
                y += 2
            else:
                x += 1
                y -= 2
        return (x, y)
        
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
        self.x_pos: int = _x
        self.y_pos: int = _y

    def __str__(self) -> str:
        return f"({self.x_pos}, {self.y_pos})"

    def abs_position(self) -> tuple:
        return (self.x_pos, self.y_pos)
    
    def map_position(self) -> tuple:
        return (Position.x_map[self.x_pos], str(self.y_pos + 1))
    
    def get_center_pixel(self) -> tuple:
        center_x = (self.x_pos * Position.MULTIPLIER) + (Position.MULTIPLIER)
        center_y = (self.y_pos * Position.MULTIPLIER) + (Position.MULTIPLIER)
        return (center_x, center_y)
    
    def x(self) -> int:
        return self.x_pos
    
    def y(self) -> int:
        return self.y_pos
    
    @staticmethod
    def map_position_index(x: int) -> str:
        return Position.x_map[x]
    
    @staticmethod
    def interpret_position(pixel_X: int, pixel_Y: int) -> tuple:
        x = math.floor((pixel_X / Position.MULTIPLIER) - 0.5)
        y = math.floor((pixel_Y / Position.MULTIPLIER) - 0.5)
        return (x, y)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x_pos == other.x() and self.y_pos == other.y()
        elif isinstance(other, tuple):
            return self.x_pos == other[0] and self.y_pos == other[1]

class Color(Enum):
    BLACK = 0
    WHITE = 1
